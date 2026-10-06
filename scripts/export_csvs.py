#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta campos.csv, indices.csv y restricciones.csv desde la BD real.
Fuente de verdad = base recreada (politica RESTRICT). Reemplaza los CSV que
quedaron con CASCADE/SET NULL (exportacion vieja) en docs/."""
import csv
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / 'docs'

# Lee credenciales del .env
env = {}
for line in (ROOT / '.env').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, _, v = line.partition('=')
        env[k.strip()] = v.strip()

USER = env['POSTGRES_USER']
DB = env['POSTGRES_DB']
PWD = env['POSTGRES_PASSWORD']

EXCLUDE = "conrelid::regclass::text NOT LIKE '%\\_2025\\_%' AND conrelid::regclass::text NOT LIKE '%\\_2026\\_%' AND conrelid::regclass::text NOT LIKE '%\\_2027\\_%' AND conrelid::regclass::text NOT LIKE '%\\_default'"


def psql(query):
    """Ejecuta query, devuelve filas como listas (separador \x1f, sin alinear)."""
    cmd = ['podman', 'exec', '-e', f'PGPASSWORD={PWD}', 'agecare-db',
           'psql', '-U', USER, '-d', DB, '-tA', '-F', '\x1f', '-c', query]
    out = subprocess.run(cmd, capture_output=True, text=True)
    rows = []
    for line in out.stdout.splitlines():
        if line.strip() == '':
            continue
        rows.append(line.split('\x1f'))
    return rows, out.stderr


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# ---- restricciones.csv ----
q_restr = f"""
SELECT conrelid::regclass::text, conname,
  CASE contype WHEN 'f' THEN 'Clave foranea' WHEN 'p' THEN 'Clave primaria'
       WHEN 'u' THEN 'Unica' WHEN 'c' THEN 'Validacion' ELSE contype::text END,
  pg_get_constraintdef(oid)
FROM pg_constraint
WHERE connamespace='public'::regnamespace AND {EXCLUDE}
ORDER BY 1, contype DESC, 2;
"""
rows, err = psql(q_restr)
n1 = write_csv(DOCS / 'restricciones.csv', ['tabla', 'restriccion', 'tipo', 'definicion'], rows)

# ---- indices.csv ----
q_idx = """
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname='public'
  AND tablename NOT LIKE '%\\_2025\\_%' AND tablename NOT LIKE '%\\_2026\\_%'
  AND tablename NOT LIKE '%\\_2027\\_%' AND tablename NOT LIKE '%\\_default'
ORDER BY tablename, indexname;
"""
rows, err = psql(q_idx)
n2 = write_csv(DOCS / 'indices.csv', ['tabla', 'indice', 'definicion'], rows)

# ---- campos.csv ----
q_col = """
SELECT c.table_name,
       obj_description((quote_ident(c.table_name))::regclass, 'pg_class'),
       c.ordinal_position, c.column_name,
       CASE WHEN c.character_maximum_length IS NOT NULL
            THEN c.data_type || '(' || c.character_maximum_length || ')'
            ELSE c.data_type END,
       CASE c.is_nullable WHEN 'NO' THEN 'NO' ELSE 'SI' END,
       COALESCE(c.column_default, ''),
       COALESCE(col_description((quote_ident(c.table_name))::regclass, c.ordinal_position), '')
FROM information_schema.columns c
JOIN information_schema.tables t
  ON t.table_name=c.table_name AND t.table_schema=c.table_schema
WHERE c.table_schema='public' AND t.table_type='BASE TABLE'
  AND c.table_name NOT LIKE '%\\_2025\\_%' AND c.table_name NOT LIKE '%\\_2026\\_%'
  AND c.table_name NOT LIKE '%\\_2027\\_%' AND c.table_name NOT LIKE '%\\_default'
ORDER BY c.table_name, c.ordinal_position;
"""
rows, err = psql(q_col)
n3 = write_csv(DOCS / 'campos.csv',
               ['tabla', 'tabla_descripcion', 'orden', 'campo', 'tipo',
                'acepta_nulo', 'valor_defecto', 'descripcion'], rows)

print(f'restricciones.csv: {n1} filas')
print(f'indices.csv: {n2} filas')
print(f'campos.csv: {n3} filas')
