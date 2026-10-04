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


def convert(md_path, docx_path):
    lines = Path(md_path).read_text(encoding='utf-8').splitlines()
    doc = Document()

    # Estilo base
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

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
