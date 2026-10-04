# AgeCare — Modelo de Datos Definitivo

**Proyecto APT · Capstone PTY4614 · DUOC UC — Sede San Andrés**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Metodología:** Enfoque Tradicional (Cascada) · **Entrega:** 04 de octubre (avance Fase 2)
**Motor:** PostgreSQL 16 · Modelo relacional normalizado hasta 2FN (excepciones técnicas documentadas)
**Scripts fuente:** `sql/001_base.sql` … `sql/501_subscriptions.sql` + `sql/900_seed_dev.sql`
**Script consolidado:** `sql/000_schema_completo.sql` (todo el esquema en un solo archivo ejecutable)
**Diagramas ER:** `docs/ER_AgeCare.dbml` (dbdiagram.io → PNG/PDF) · `docs/ER_AgeCare_Mermaid.md` (se renderiza en GitHub)
**Análisis de realidad:** `docs/04_Analisis_de_Realidad_y_Decisiones.md` (escenarios del mundo real y decisiones de diseño)

---

## 1. Propósito y alcance

Este documento presenta el **modelo de datos definitivo** del núcleo de salud de AgeCare, como
evidencia del avance de Fase 2 comprometido para el 04 de octubre. El modelo da soporte físico
a los requisitos del ERS correspondientes a autenticación, pacientes y círculo de cuidado,
signos vitales, medicamentos y adherencia, y alertas/emergencias (**RF-01 a RF-33 y RF-44 a
RF-52**), junto con los requisitos no funcionales de rendimiento, escalabilidad, seguridad y
mantenibilidad asociados.

El diseño es íntegramente **relacional en PostgreSQL** (no existe persistencia documental ni
NoSQL): los pocos campos `jsonb` que persisten corresponden a atributos variables documentados
como excepción. El equipo construyó las 24 tablas en este repositorio como consultores/
desarrolladores sobre la especificación de Alloxentric.

A las tablas del núcleo se suman cuatro tablas transversales derivadas del **análisis de
realidad** (ver documento 04): `audit_log` (trazabilidad clínica inmutable), `system_parameters`
(umbrales de negocio configurables), `wellbeing_snapshots` (historial del semáforo) y
`subscriptions` (modelo freemium).

---

## 2. Bloques del modelo

| Bloque | Tablas | RF que soporta |
|---|---|---|
| **1 · Identidad y acceso** | `users`, `refresh_tokens`, `push_devices`, `patients`, `patient_conditions`, `patient_members`, `invitations`, `audit_log`, `system_parameters` | RF-01…16, RNF-14 |
| **2 · Vitals y wearable** | `vital_types`, `wearables`, `vital_readings`, `vital_thresholds`, `wellbeing_snapshots` | RF-15…23, RF-44 |
| **3 · Medicación** | `medications`, `medication_times`, `medication_days`, `scheduled_doses` | RF-24…33 |
| **4 · Alertas y emergencias** | `alerts`, `alert_deliveries`, `notification_settings`, `emergency_contacts`, `sos_events` | RF-44…52 |
| **5 · Negocio (freemium)** | `subscriptions` | RF-73 |

**Total: 24 tablas** + función compartida `set_updated_at()` + función de particionado + trigger de inmutabilidad de auditoría.

---

## 3. Diagrama de relaciones (texto)

```
users ──1:N── refresh_tokens
  │   ├─1:N── push_devices
  │   ├─1:N── patient_members ──N:1── patients
  │   ├─1:N── notification_settings
  │   └─ (invited_by / accepted_by) ── invitations

patients ──1:N── patient_conditions
  │   ├─1:N── patient_members          (centro del control de acceso, RNF-12)
  │   ├─1:N── invitations
  │   ├─1:N── wearables
  │   ├─1:N── vital_readings ──N:1── vital_types
  │   ├─1:N── vital_thresholds ──N:1── vital_types
  │   ├─1:N── medications ──1:N── medication_times
  │   │                     └─1:N── medication_days
  │   ├─1:N── alerts
  │   ├─1:N── emergency_contacts
  │   └─1:N── sos_events

medications ──1:N── scheduled_doses ──(logged_by)── users
alerts ──1:N── alert_deliveries ──N:1── users / push_devices
alerts ──1:1── sos_events
```

**Regla transversal (RNF-12):** toda consulta al expediente se valida contra
`patient_members` (membresía vigente + rol). Ocultar la opción en la interfaz no se considera
control de acceso.

---

## 4. Tablas y su correspondencia con el ERS

### Bloque 1 — Identidad y acceso

| Tabla | Propósito | RF |
|---|---|---|
| `users` | Cuentas. `first_name`+`last_name`, `full_name` GENERATED. `password_hash` (RNF-10). Soft delete. | RF-01, RF-06 |
| `refresh_tokens` | Sesiones; hash del token, `family_id` para revocación rotatoria (RNF-11). | RF-02…05 |
| `push_devices` | Dispositivos para notificaciones; `push_token` único. | RF-07 |
| `patients` | Adultos mayores (no son usuarios). `rut`, `timezone`, soft delete. | RF-08…10 |
| `patient_conditions` | Condiciones médicas (1FN; reemplaza arreglo JSON). | RF-08 |
| `patient_members` | Vínculo usuario↔paciente con rol; `is_owner`. Control de acceso. | RF-11…14, RF-12 |
| `invitations` | Invitaciones por correo; token hasheado con vencimiento. | RF-11, RF-13 |
| `audit_log` | Registro inmutable (append-only) de accesos y cambios clínicos; trigger bloquea UPDATE/DELETE. | RNF-14 |
| `system_parameters` | Catálogo de umbrales de negocio configurables (fuera del código). | RF-33, RF-52, RNF-11, RNF-13 |

### Bloque 2 — Vitals y wearable

| Tabla | Propósito | RF |
|---|---|---|
| `vital_types` | Catálogo de tipos de signos vitales (fuente única de verdad). | RF-17…21 |
| `wearables` | Dispositivo vinculado; `last_sync_at`, `battery_pct`. | RF-15, RF-16 |
| `vital_readings` | Mediciones; particionada por mes (RNF-07); idempotente (RNF-08); CHECK de cordura de valores. | RF-17…20, RF-22, RF-44 |
| `vital_thresholds` | Rango normal por paciente y tipo. | RF-21 |
| `wellbeing_snapshots` | Fotografía diaria del semáforo (historiza el indicador que antes se calculaba al vuelo). | RF-22 |

### Bloque 3 — Medicación

| Tabla | Propósito | RF |
|---|---|---|
| `medications` | Plan de medicamento; dosis estructurada (`dose_amount` + `dose_unit`, `dose_text` GENERATED). | RF-24…27 |
| `medication_times` | Horarios de toma (1FN). | RF-24, RF-32 |
| `medication_days` | Días habilitados (1FN). | RF-24, RF-32 |
| `scheduled_doses` | Tomas y estado; sin `patient_id` (2FN, JOIN); 3 momentos: `scheduled_at`/`administered_at`/`logged_at`. | RF-28…30, RF-32, RF-33 |

### Bloque 4 — Alertas y emergencias

| Tabla | Propósito | RF |
|---|---|---|
| `alerts` | Alertas del sistema; `dedup_key` evita repetidas (RF-46). | RF-44, RF-47…49 |
| `alert_deliveries` | Un registro por intento de notificación; mide latencia (RNF-05). | RF-45 |
| `notification_settings` | Preferencias por tipo; caída y emergencia no desactivables. | RF-50 |
| `emergency_contacts` | Contactos en orden de escalamiento; `first_name`+`last_name` (1FN). | RF-51, RF-52 |
| `sos_events` | Activaciones del botón de emergencia; una por alerta; ubicación. | RF-51 |

### Bloque 5 — Negocio (freemium)

| Tabla | Propósito | RF |
|---|---|---|
| `subscriptions` | Suscripción del modelo freemium; una activa por usuario; `provider_ref` opaco (sin datos de tarjeta). | RF-73 |

---

## 5. Estado de normalización

### Correcciones aplicadas (hasta 2FN)

| Tabla | Antes | Después |
|---|---|---|
| `patients` / `users` | `full_name` no atómico | `first_name` + `last_name` + GENERATED |
| `patients` | `conditions` jsonb | tabla `patient_conditions` |
| `medications` | `times` + `days_of_week` jsonb | `medication_times` + `medication_days` |
| `scheduled_doses` | `patient_id` redundante (2FN) | eliminado; se usa JOIN con `medications` |
| `alerts` | `update_at` (typo, rompía el trigger) | `updated_at` |
| `vital_readings` / `vital_thresholds` | `CHECK` de tipo duplicado | catálogo `vital_types` + FK |
| `push_devices` | trigger `updated_at` faltante | trigger agregado |
| `emergency_contacts` | `full_name` no atómico | `first_name` + `last_name` + GENERATED |
| `medications` | `dose` varchar ("50 mg") no computable | `dose_amount` numérico + `dose_unit` + `dose_text` GENERATED |
| `scheduled_doses` | `logged_at` confundía hecho clínico y registro | se agrega `administered_at` (hora real de administración) |

### Excepciones documentadas (decisión de diseño, no error)

| Caso | Motivo |
|---|---|
| `vital_readings` PK `(id, measured_at)` | PostgreSQL exige la columna de particionamiento en la PK. |
| `alerts.payload` jsonb | Atributos variables según el tipo de alerta; no se consultan ni cruzan. |
| `vital_readings.meta` jsonb | Cada proveedor de wearable envía campos distintos; solo trazabilidad. |
| `patients.rut_dv` | Derivable de `rut_number` (módulo 11); se guarda por conveniencia de validación. |

Detalle completo en `docs/Normalizacion_2FN_AgeCare.md`.

---

## 6. Matriz de cobertura — Modelo ↔ Requisitos del ERS (transparencia)

| Módulo del ERS | RF | Tablas | Cobertura |
|---|---|---|---|
| Autenticación y cuentas | RF-01…07 | `users`, `refresh_tokens`, `push_devices` | ✅ 100% |
| Pacientes y círculo | RF-08…16 | `patients`, `patient_conditions`, `patient_members`, `invitations`, `wearables` | ✅ 100% |
| Salud y signos vitales | RF-17…23 | `vital_types`, `vital_readings`, `vital_thresholds`, `wearables` | ✅ 100% |
| Medicamentos y adherencia | RF-24…33 | `medications`, `medication_times`, `medication_days`, `scheduled_doses` | ✅ 100% (OCR RF-31 es lógica de app, no requiere tabla nueva) |
| Alertas y emergencias | RF-44…52 | `alerts`, `alert_deliveries`, `notification_settings`, `emergency_contacts`, `sos_events`, `system_parameters` | ✅ 100% |
| Operación de la cuidadora (freemium) | RF-73 | `subscriptions` | ✅ Base de datos lista (validación en app) |
| Trazabilidad clínica | RNF-14 | `audit_log` | ✅ 100% |
| Bitácora del expediente | RF-34…38 | *Fase 2 (resto)* | ⏳ |
| Archivos y documentos | RF-39…43 | *Fase 2 (resto)* | ⏳ |
| Comunicación + Asistente IA | RF-53…59 | *Fase 2 (resto)* | ⏳ |
| Vista del adulto mayor (+ Director Musical) | RF-60…69 | *Fase 2 (resto)* | ⏳ |
| Operación de la cuidadora (resto) | RF-70…72, RF-74 | *Fase 2 (resto)* | ⏳ |
| Marketplace | RF-75…79 | *Fase 2 (resto)* | ⏳ |
| Funcionamiento sin conexión | RF-80…82 | *Fase 2 (resto, lado app)* | ⏳ |

### Conclusión de cobertura

- **El núcleo de salud (RF-01…33 y RF-44…52) está 100% soportado** por el modelo definitivo
  (24 tablas). Este es el avance comprometido para el 04 de octubre.
- Las cuatro tablas transversales (`audit_log`, `system_parameters`, `wellbeing_snapshots`,
  `subscriptions`) nacen del **análisis de realidad** (documento 04): resuelven trazabilidad
  clínica (RNF-14), configurabilidad de umbrales, memoria histórica del bienestar y base del
  modelo freemium (RF-73).
- Los módulos restantes del ERS están **especificados y declarados**; se incorporan en el resto
  de la Fase 2 siguiendo el patrón ya establecido (FK a `patients`/`users`, control por
  `patient_members`), sin rediseñar el núcleo.

---

## 7. Orden de carga de scripts (dependencias de FK)

```
001_base              función set_updated_at
101_users             → base de todo
102_refresh_tokens    → users
103_push_devices      → users
104_patients          + patient_conditions
105_patient_members   → patients, users
106_invitations       → patients, users
107_audit_log         → users, patients (trazabilidad inmutable)
108_system_parameters → users (parámetros de negocio)
200_vital_types       catálogo (antes de 202/203)
201_wearables         → patients
202_vital_readings    → patients, vital_types   (particionada por mes)
203_vital_thresholds  → patients, vital_types
204_wellbeing_snapshots → patients (historial del semáforo)
301_medications       + medication_times + medication_days → patients
302_scheduled_doses   → medications, users
401_alerts            → patients, users
402_alert_deliveries  → alerts, users, push_devices
403_notification_settings → users
404_emergency_contacts → patients
405_sos_events        → patients, users, alerts
501_subscriptions     → users (modelo freemium)
900_seed_dev          datos de demostración
```

El prefijo numérico garantiza que cada tabla padre preceda a sus claves foráneas: `users` y
`patients` antes de `audit_log`/`system_parameters`, `vital_types` (200) antes de las tablas
que lo referencian (202, 203), y así sucesivamente. Este encadenamiento explícito es coherente
con el orden secuencial propio de la metodología en cascada.
