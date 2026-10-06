#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruye el schema consolidado desde los scripts numerados de sql/.
Fuente unica de verdad = scripts numerados. El consolidado es su concatenacion
en orden de dependencias de FK. Evita que el consolidado quede desincronizado
(como paso tras el cambio a ON DELETE RESTRICT)."""
from pathlib import Path

ROOT = Path(__file__).parent.parent
SQL = ROOT / 'sql'

# Orden de dependencias de FK (mismo del consolidado original, sin el seed).
ORDER = [
    '001_base.sql',
    '101_users.sql', '102_refresh_tokens.sql', '103_push_devices.sql',
    '104_patients.sql', '105_patient_members.sql', '106_invitations.sql',
    '107_audit_log.sql', '108_system_parameters.sql',
    '200_vital_types.sql', '201_wearables.sql', '202_vital_readings.sql',
    '203_vital_thresholds.sql', '204_wellbeing_snapshots.sql',
    '301_medications.sql', '302_scheduled_doses.sql',
    '401_alerts.sql', '402_alert_deliveries.sql', '403_notification_settings.sql',
    '404_emergency_contacts.sql', '405_sos_events.sql',
    '501_subscriptions.sql',
]

HEADER = """-- AgeCare - Esquema completo consolidado (modelo de datos definitivo)
-- Proyecto APT - Capstone PTY4614 - DUOC UC
-- PostgreSQL 16 - Modelo relacional normalizado hasta 2FN
--
-- Consolida los scripts de esquema del directorio sql/ en orden de
-- dependencias de claves foraneas. El seed (900_seed_dev.sql) va aparte.
-- 24 tablas de negocio + funciones y triggers.
--
-- GENERADO automaticamente por scripts/build_consolidado.py desde los
-- scripts numerados. No editar a mano: editar los numerados y regenerar.
-- ============================================================================

"""

SEP = ("\n\n-- ============================================================================\n"
       "-- Fuente: {name}\n"
       "-- ============================================================================\n")


def build():
    parts = [HEADER]
    for name in ORDER:
        path = SQL / name
        content = path.read_text(encoding='utf-8')
        parts.append(SEP.format(name=name))
        parts.append(content.rstrip() + '\n')
    return ''.join(parts)


if __name__ == '__main__':
    out = build()
    targets = [
        SQL / 'schema' / '000_schema_completo.sql',
        ROOT / 'docs' / '000_schema_completo.sql',
        ROOT / 'entrega_fase2' / 'Evidencias Proyecto' / '08_schema_completo.sql',
    ]
    for t in targets:
        t.write_text(out, encoding='utf-8')
        print('escrito', t.relative_to(ROOT))
    print('OK consolidado regenerado desde', len(ORDER), 'scripts numerados')
