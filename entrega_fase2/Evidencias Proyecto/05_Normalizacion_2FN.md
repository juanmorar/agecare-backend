# AgeCare — Análisis y Corrección de Normalización (hasta 2FN)

Revisión del esquema SQL (`sql/`) contra la Primera y Segunda Forma Normal,
con el estado de cada corrección **ya aplicada** al repositorio.

---

## Conceptos aplicados

| Forma Normal | Regla |
|---|---|
| **1FN** | Cada celda contiene un valor atómico. No hay grupos repetidos ni arreglos multivaluados. Existe clave primaria. |
| **2FN** | Cumple 1FN + cada atributo no-clave depende de **toda** la clave primaria, no de una parte. Aplica cuando la PK es compuesta. |

---

## Estado de las pifias

| # | Tabla | Problema | Gravedad | Estado |
|---|---|---|---|---|
| 1 | `patients` | `conditions` arreglo JSON (1FN) | 🔴 Alta | ✅ Corregido → `patient_conditions` |
| 2 | `patients` | `full_name` no atómico (1FN) | 🟡 Media | ✅ Corregido → `first_name` + `last_name` |
| 3 | `patients` | `rut_dv` derivable de `rut_number` | 🟢 Baja | ✅ Documentado como derivado |
| 4 | `medications` | `times` + `days_of_week` JSON (1FN) | 🔴 Alta | ✅ Corregido → `medication_times` + `medication_days` |
| 5 | `scheduled_doses` | `patient_id` dependencia parcial (2FN) | 🔴 Alta | ✅ Corregido → eliminado, se usa JOIN |
| 6 | `alerts` | `update_at` typo (rompía el trigger) | 🟡 Media | ✅ Corregido → `updated_at` |
| 7 | `alerts` | `payload` JSON sin estructura (1FN) | 🟡 Media | ✅ Documentado como excepción justificada |
| 8 | `vital_readings` | PK compuesta `(id, measured_at)` (2FN) | 🔴 Alta | ✅ Documentado como excepción técnica |
| 9 | `vital_readings` | `meta` JSON sin estructura (1FN) | 🟢 Baja | ✅ Documentado como excepción justificada |
| 10 | `vital_thresholds` | `CHECK` de `type` duplicado | 🟡 Media | ✅ Corregido → catálogo `vital_types` |
| 11 | `users` | `full_name` no atómico (1FN) | 🟡 Media | ✅ Corregido → `first_name` + `last_name` |
| 12 | `push_devices` | trigger `updated_at` faltante | 🟢 Baja | ✅ Corregido → trigger agregado |
| 13 | `emergency_contacts` | `full_name` no atómico (1FN) | 🟡 Media | ✅ Corregido → `first_name` + `last_name` |
| 14 | `medications` | `dose` varchar "50 mg" no computable (1FN) | 🟡 Media | ✅ Corregido → `dose_amount` + `dose_unit` |
| 15 | `scheduled_doses` | `logged_at` confundía hecho clínico y registro | 🔴 Alta | ✅ Corregido → se agrega `administered_at` |

**Total: 15 pifias — 11 corregidas estructuralmente, 4 documentadas como excepción justificada.**

> Las correcciones 13 a 15 provienen del **análisis de realidad** (documento 04): surgieron al
> evaluar escenarios del mundo real (negligencia humana, registro tardío de dosis, coherencia
> de nombres) más allá de la revisión formal de formas normales.

---

## Correcciones estructurales aplicadas

### 1. `patient_conditions` (reemplaza `patients.conditions`)
```sql
CREATE TABLE patient_conditions (
    id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    condition  varchar(80) NOT NULL,
    diagnosed_at date,
    CONSTRAINT uq_patient_condition UNIQUE (patient_id, condition)
);
```
Cada condición médica es una fila atómica. Permite filtrar e indexar por padecimiento y guardar fecha de diagnóstico.

### 2 y 11. `first_name` + `last_name` en `patients` y `users`
```sql
first_name varchar(60) NOT NULL,
last_name  varchar(60) NOT NULL,
full_name  varchar(121) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
```
`full_name` se mantiene como columna **calculada** (solo lectura) para no romper el contrato de la API v1.

### 4. `medication_times` + `medication_days` (reemplazan los JSON de `medications`)
```sql
CREATE TABLE medication_times (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    medication_id uuid NOT NULL REFERENCES medications(id) ON DELETE CASCADE,
    time_of_day   time NOT NULL,
    UNIQUE (medication_id, time_of_day)
);
CREATE TABLE medication_days (
    medication_id uuid NOT NULL REFERENCES medications(id) ON DELETE CASCADE,
    day_of_week   smallint CHECK (day_of_week BETWEEN 1 AND 7),
    PRIMARY KEY (medication_id, day_of_week)
);
```

### 5. `scheduled_doses` sin `patient_id`
Columna eliminada (era dependencia parcial de `medication_id`). Las consultas por paciente hacen:
```sql
JOIN medications m ON m.id = sd.medication_id WHERE m.patient_id = :pid
```

### 6. `alerts.update_at` → `updated_at`
El trigger `tg_alerts_updated_at` escribe en `updated_at`; con el typo nunca funcionaba. Renombrado.

### 10. Catálogo `vital_types`
```sql
CREATE TABLE vital_types (
    code varchar(16) PRIMARY KEY,
    label varchar(60) NOT NULL,
    unit  varchar(10) NOT NULL DEFAULT '',
    has_secondary boolean NOT NULL DEFAULT false
);
```
`vital_readings.type` y `vital_thresholds.type` ahora son FK a `vital_types.code`. Fuente única de verdad; elimina el `CHECK` duplicado y el dict `UNITS` hardcodeado en `vitals.py`.

### 12. Trigger en `push_devices`
```sql
CREATE TRIGGER tg_push_devices_updated_at
    BEFORE UPDATE ON push_devices
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

## Excepciones documentadas (no se corrigen por diseño)

### 8. `vital_readings` PK `(id, measured_at)` — excepción TÉCNICA
PostgreSQL **exige** que la columna de particionamiento (`measured_at`) forme parte de la PK en tablas `PARTITION BY RANGE`. En el modelo relacional puro la PK sería solo `id`. Documentado en el constraint:
```sql
COMMENT ON CONSTRAINT pk_vital_readings ON vital_readings IS
    'PK compuesta por requerimiento técnico de PostgreSQL para tablas
     particionadas. No implica dependencia funcional en measured_at.';
```

### 7 y 9. `alerts.payload` y `vital_readings.meta` — excepción JUSTIFICADA
Son JSON de **atributos variables**: su estructura cambia según el tipo de alerta o el proveedor del wearable. Normalizarlos exigiría una tabla de detalle por cada tipo/proveedor, sin ganar integridad porque esos datos **no se consultan ni se cruzan**, solo se muestran. Documentado en cada columna como excepción a 1FN.

### 3. `patients.rut_dv` — dato derivado documentado
El dígito verificador se calcula desde `rut_number` por módulo 11. Se almacena por conveniencia de validación; documentado como derivado.

---

## Archivos de código adaptados al nuevo esquema

| Archivo | Cambio |
|---|---|
| `api/app/routers/auth.py` | `first_name` + `last_name` en register/login/get_me/patch_me |
| `api/app/routers/patients.py` | `patient_conditions`; nombre dividido |
| `api/app/routers/medications.py` | `medication_times`/`medication_days`; dosis sin `patient_id` (JOIN) |
| `api/app/routers/vitals.py` | `UNITS` → `_get_unit()` desde `vital_types`; `_medications_today` con JOIN |
| `sql/900_seed_dev.sql` | Datos de demo reescritos al esquema normalizado |
| `front/test.html` + `api/app/static/test.html` | Formularios usan `first_name`/`last_name` |
| `TESTING.md` | Ejemplos JSON actualizados |

---

## Orden de ejecución de los scripts (importante)

Los `.sql` corren en orden alfabético. El catálogo `vital_types` (`200_`) **debe** ejecutarse
antes de `vital_readings` (`202_`) y `vital_thresholds` (`203_`) porque ambos lo referencian
por FK. El orden actual lo garantiza:

```
001_base → 101_users → … → 106_invitations →
200_vital_types → 201_wearables → 202_vital_readings → 203_vital_thresholds →
301_medications → 302_scheduled_doses → 401_alerts → … → 900_seed_dev
```

---

## Lo que ya estaba bien

- Todas las tablas tienen PK (`uuid`). ✅
- Foreign keys con política correcta (`CASCADE` / `SET NULL`). ✅
- Índices parciales (`WHERE deleted_at IS NULL`) correctos. ✅
- Soft-delete en registros clínicos. ✅
- Partición mensual de `vital_readings` justificada por volumen (RNF-07). ✅
