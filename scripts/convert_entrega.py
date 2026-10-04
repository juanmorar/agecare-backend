#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte todos los .md de entrega_fase2/ a .docx (misma carpeta)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from md_to_docx import convert

ROOT = Path(__file__).parent.parent
ENTREGA = ROOT / 'entrega_fase2'

results = []
for md in sorted(ENTREGA.rglob('*.md')):
    docx = md.with_suffix('.docx')
    try:
        convert(str(md), str(docx))
        results.append(('OK', str(docx.relative_to(ROOT))))
    except Exception as e:
        results.append(('FAIL', f'{md.relative_to(ROOT)} :: {e}'))

for status, path in results:
    print(status, path)
print('TOTAL', len(results))
