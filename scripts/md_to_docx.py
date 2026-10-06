#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor Markdown -> DOCX para la entrega Fase 2 de AgeCare.

Maneja:
- Encabezados # .. ######
- Párrafos con inline **negrita**, *itálica*, `código`
- Listas con viñetas (-, *) y numeradas (1.)  (con sangría por nivel)
- Tablas pipe  | a | b |  con fila de separación |---|---|
- Bloques de código ```...```
- Separadores horizontales ---
- Citas > ...

No depende de pandoc. Usa python-docx.
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INLINE_RE = re.compile(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)')

# Artefactos de exportacion desde Google Docs / Pandoc:
#  - anclas al final de titulos:  "# **1. Introduccion** {#introduccion}"
#  - enlaces de indice rotos:     "[1. Introduccion 3](#_heading=)"
HEADING_ANCHOR_RE = re.compile(r'\s*\{#[^}]*\}\s*$')
TOC_LINK_RE = re.compile(r'\[([^\]]*?)\s*\d*\]\(#_?[^)]*\)')


def clean_gdocs_artifacts(text):
    """Quita anclas {#...} de titulos y convierte enlaces de indice rotos
    [Texto 3](#_heading=) en texto plano 'Texto'."""
    text = HEADING_ANCHOR_RE.sub('', text)
    # enlaces de indice: dejar solo el texto, sin el numero de pagina ni el link
    text = TOC_LINK_RE.sub(lambda m: m.group(1).strip(), text)
    return text


def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def add_inline(paragraph, text):
    """Agrega texto a un párrafo interpretando **bold**, *italic*, `code`."""
    parts = INLINE_RE.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith('*') and part.endswith('*'):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        elif part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0xC7, 0x25, 0x4E)
        else:
            paragraph.add_run(part)


def is_table_sep(line):
    s = line.strip()
    if not s.startswith('|'):
        return False
    return bool(re.match(r'^\|?[\s:|-]+\|?$', s)) and '-' in s


def parse_table_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def add_table(doc, rows):
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=0, cols=ncols)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for j in range(ncols):
            txt = row[j] if j < len(row) else ''
            cell = cells[j]
            cell.paragraphs[0].text = ''
            p = cell.paragraphs[0]
            add_inline(p, txt)
            if i == 0:
                set_cell_background(cell, '2E5A88')
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def add_code_block(doc, code_lines):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run('\n'.join(code_lines))
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1E, 0x1E, 0x1E)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)


def add_hr(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'A0A0A0')
    pbdr.append(bottom)
    pPr.append(pbdr)


def _set_field(paragraph, instr):
    """Inserta un campo de Word (ej. PAGE, TOC) en un parrafo."""
    run = paragraph.add_run()
    fldBegin = OxmlElement('w:fldChar'); fldBegin.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = instr
    fldSep = OxmlElement('w:fldChar'); fldSep.set(qn('w:fldCharType'), 'separate')
    fldEnd = OxmlElement('w:fldChar'); fldEnd.set(qn('w:fldCharType'), 'end')
    run._r.append(fldBegin); run._r.append(instrText); run._r.append(fldSep); run._r.append(fldEnd)


def add_page_number_footer(doc):
    """Pie de pagina con 'Pagina X' centrado, en todas las secciones."""
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run('Página '); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
        _set_field(p, 'PAGE')


def add_cover_page(doc, title, subtitle=None):
    """Portada: logo textual, titulo del documento, datos del equipo."""
    for _ in range(5):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('AgeCare'); r.bold = True; r.font.size = Pt(30); r.font.color.rgb = RGBColor(0x2E, 0x5A, 0x88)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('Plataforma digital integral de cuidado de adultos mayores')
    r.italic = True; r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title); r.bold = True; r.font.size = Pt(18)
    if subtitle:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(subtitle); r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    for _ in range(6):
        doc.add_paragraph()
    datos = [
        'Proyecto APT · Capstone PTY4614',
        'Duoc UC · Escuela de Informática y Telecomunicaciones · Sede San Andrés de Concepción',
        'Empresa contraparte: Alloxentric',
        'Equipo: Javier Cerna Chávez · Benjamín Camus · Juan Mora',
        'Docentes: Jazna Meza Hidalgo · Juan Pablo Mellado Alarcón',
    ]
    for d in datos:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(d); r.font.size = Pt(11)
    doc.add_page_break()


def add_toc(doc):
    """Indice automatico (campo TOC de Word, se actualiza al abrir)."""
    h = doc.add_paragraph(); r = h.add_run('Índice'); r.bold = True; r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(0x2E, 0x5A, 0x88)
    p = doc.add_paragraph()
    _set_field(p, 'TOC \\o "1-3" \\h \\z \\u')
    note = doc.add_paragraph()
    rr = note.add_run('(Clic derecho → Actualizar campos para numerar el índice)')
    rr.italic = True; rr.font.size = Pt(8); rr.font.color.rgb = RGBColor(0xA0, 0xA0, 0xA0)
    doc.add_page_break()


def convert(md_path, docx_path):
    lines = Path(md_path).read_text(encoding='utf-8').splitlines()
    doc = Document()

    # Estilo base
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    style.paragraph_format.line_spacing = 1.5

    # Extraer titulo del documento: primer encabezado '# ...'
    doc_title = None
    for ln in lines:
        m = re.match(r'^#\s+(.+)$', ln.strip())
        if m:
            doc_title = clean_gdocs_artifacts(m.group(1)).replace('*', '').strip()
            break
    if not doc_title:
        doc_title = Path(md_path).stem

    # Portada + indice + paginacion
    add_cover_page(doc, doc_title, 'Avance Fase 2 · Diseño del Sistema')
    add_toc(doc)
    add_page_number_footer(doc)

    i = 0
    n = len(lines)
    pending_list_num = {}
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # No tocar el contenido dentro de bloques de codigo
        if not stripped.startswith('```'):
            cleaned = clean_gdocs_artifacts(stripped)
            if cleaned != stripped:
                stripped = cleaned
                line = cleaned

        # Bloque de código
        if stripped.startswith('```'):
            code = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            add_code_block(doc, code)
            i += 1
            continue

        # Tabla
        if stripped.startswith('|') and i + 1 < n and is_table_sep(lines[i + 1]):
            header = parse_table_row(line)
            rows = [header]
            i += 2  # saltar separador
            while i < n and lines[i].strip().startswith('|'):
                rows.append(parse_table_row(lines[i]))
                i += 1
            add_table(doc, rows)
            doc.add_paragraph()
            continue

        # Separador horizontal
        if stripped in ('---', '***', '___'):
            add_hr(doc)
            i += 1
            continue

        # Encabezados
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            h = doc.add_heading(level=min(level, 4))
            add_inline(h, text)
            i += 1
            continue

        # Cita
        if stripped.startswith('> '):
            p = doc.add_paragraph(style='Intense Quote')
            add_inline(p, stripped[2:])
            i += 1
            continue

        # Lista numerada
        mnum = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if mnum:
            p = doc.add_paragraph(style='List Number')
            indent = len(mnum.group(1))
            if indent >= 2:
                p.paragraph_format.left_indent = Inches(0.25 * (indent // 2))
            add_inline(p, mnum.group(3))
            i += 1
            continue

        # Lista con viñetas
        mbul = re.match(r'^(\s*)[-*]\s+(.*)$', line)
        if mbul:
            p = doc.add_paragraph(style='List Bullet')
            indent = len(mbul.group(1))
            if indent >= 2:
                p.paragraph_format.left_indent = Inches(0.25 * (indent // 2))
            add_inline(p, mbul.group(2))
            i += 1
            continue

        # Línea vacía
        if stripped == '':
            i += 1
            continue

        # Párrafo normal
        p = doc.add_paragraph()
        add_inline(p, stripped)
        i += 1

    doc.save(docx_path)
    return docx_path


if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    out = convert(src, dst)
    print('OK', out)
