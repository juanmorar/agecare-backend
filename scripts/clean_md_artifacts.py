#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Limpia artefactos de exportacion Google Docs/Pandoc en los .md de la entrega
(anclas {#...} en titulos y enlaces de indice rotos (#_heading=)) y deja el .md
tal cual se vera en el .docx. Solo reescribe archivos que realmente cambian."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from md_to_docx import clean_gdocs_artifacts, HEADING_ANCHOR_RE, TOC_LINK_RE

ROOT = Path(__file__).parent.parent
ENTREGA = ROOT / 'entrega_fase2'


def clean_file(path):
    original = path.read_text(encoding='utf-8')
    out_lines = []
    changed = False
    in_code = False
    for line in original.splitlines():
        if line.strip().startswith('```'):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue
        new = clean_gdocs_artifacts(line)
        if new != line:
            changed = True
        out_lines.append(new)
    if changed:
        path.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
    return changed


results = []
for md in sorted(ENTREGA.rglob('*.md')):
    try:
        changed = clean_file(md)
        results.append(('CHANGED' if changed else 'ok', str(md.relative_to(ROOT))))
    except Exception as e:
        results.append(('FAIL', f'{md.relative_to(ROOT)} :: {e}'))

for status, path in results:
    print(status, path)
print('TOTAL', len(results))
