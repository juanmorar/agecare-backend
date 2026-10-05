# AgeCare — Diccionario de Datos

**Proyecto APT · Capstone PTY4614 · DUOC UC — Grupo 1**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Motor:** PostgreSQL 16 · Modelo relacional normalizado hasta 2FN
**Fuente:** `sql/schema/000_schema_completo.sql` (24 tablas)

---

## Convenciones

- **PK:** clave primaria · **FK:** clave foránea · **UK:** restricción única · **NN:** no nulo.
- Los tipos corresponden a PostgreSQL: `uuid`, `varchar(n)`, `text`, `timestamptz` (fecha-hora
  con zona), `date`, `time`, `numeric(p,e)`, `smallint`, `boolean`, `jsonb`, `inet`.
- "GENERATED" indica columna calculada por la base (solo lectura).
- Política de borrado en FK: `CASCADE` (borra en cascada) o `SET NULL` (anula la referencia).

---

## Bloque 1 — Identidad y acceso

### Tabla: `users` — Cuentas de usuario del sistema

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador interno de la cuenta. |
| email | varchar(254) | NN, UK (sin mayúsculas) | Correo de acceso. |
| password_hash | varchar(255) | NN | Hash de la contraseña (bcrypt/argon2). Nunca texto plano. |
| first_name | varchar(60) | NN | Nombre(s) del usuario. |
| last_name | varchar(60) | NN | Apellido(s) del usuario. |
| full_name | varchar(121) | GENERATED | Nombre completo calculado (first + last). Solo lectura. |
| phone | varchar(16) | | Teléfono en formato E.164. Opcional. |
| avatar_url | text | | URL de la foto de perfil. Opcional. |
| locale | varchar(5) | NN, def. 'es' | Idioma de la interfaz (es/en). |
| is_active | boolean | NN, def. true | false = cuenta desactivada por soporte. |
| created_at | timestamptz | NN | Fecha de creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |
| deleted_at | timestamptz | | Baja lógica (soft delete). NULL = vigente. |

### Tabla: `refresh_tokens` — Sesiones activas (tokens de refresco)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del registro de sesión. |
| user_id | uuid | FK → users (CASCADE), NN | Dueño de la sesión. |
| family_id | uuid | NN | Agrupa los tokens de un mismo inicio de sesión (rotación). |
| token_hash | varchar(64) | NN, UK | SHA-256 del token. Nunca el token en claro. |
| expires_at | timestamptz | NN | Vencimiento (30 días). |
| revoked_at | timestamptz | | Momento de revocación. NULL = vigente. |
| revoked_reason | varchar(20) | | Motivo: rotated/logout/reuse_detected/… |
| created_at | timestamptz | NN | Emisión del token. |

### Tabla: `push_devices` — Dispositivos para notificaciones push

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del dispositivo. |
| user_id | uuid | FK → users (CASCADE), NN | Dueño actual del dispositivo. |
| push_token | varchar(255) | NN, UK | Token de FCM/APNs. Identifica la instalación. |
| platform | varchar(10) | NN | ios / android / web. |
| is_active | boolean | NN, def. true | false = sesión cerrada o token inválido. |
| last_seen_at | timestamptz | NN | Última confirmación del dispositivo. |
| created_at | timestamptz | NN | Primer registro. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

### Tabla: `patients` — Adultos mayores con expediente

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del paciente. |
| first_name | varchar(60) | NN | Nombre(s) del adulto mayor. |
| last_name | varchar(60) | NN | Apellido(s) del adulto mayor. |
| full_name | varchar(121) | GENERATED | Nombre completo calculado. Solo lectura. |
| rut_number | integer | | RUT sin puntos ni dígito verificador. |
| rut_dv | char(1) | | Dígito verificador (0-9 o K). Derivable de rut_number. |
| birth_date | date | NN | Fecha de nacimiento. La edad se calcula. |
| sex | char(1) | NN | M / F / O. |
| photo_url | text | | Foto del paciente. Opcional. |
| timezone | varchar(50) | NN, def. 'America/Santiago' | Zona horaria IANA (horarios de medicación). |
| created_at | timestamptz | NN | Creación del expediente. |
| updated_at | timestamptz | NN | Última modificación (trigger). |
| deleted_at | timestamptz | | Baja lógica. NULL = vigente. |

### Tabla: `patient_conditions` — Condiciones médicas del paciente

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la condición. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente al que pertenece. |
| condition | varchar(80) | NN, UK (patient_id, condition) | Padecimiento (ej. hipertension). |
| diagnosed_at | date | | Fecha de diagnóstico. Opcional. |
| created_at | timestamptz | NN | Fecha de registro. |

### Tabla: `patient_members` — Vínculo usuario↔paciente con rol (control de acceso)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del vínculo. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| user_id | uuid | FK → users (CASCADE), NN | Usuario. |
| role | varchar(10) | NN | family / caregiver / doctor / elder. |
| is_owner | boolean | NN, def. false | Administrador del paciente (solo rol family). |
| created_at | timestamptz | NN | Alta del vínculo. |
| updated_at | timestamptz | NN | Última modificación (trigger). |
| removed_at | timestamptz | | Baja del círculo. Conserva historial. |

*UK: (patient_id, user_id). Índice único de un solo owner por paciente.*

### Tabla: `invitations` — Invitaciones al círculo de cuidado

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la invitación. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente al que se invita. |
| email | varchar(320) | NN | Correo del invitado (puede no tener cuenta). |
| role | varchar(10) | NN | Rol a asignar: family/caregiver/doctor/elder. |
| token_hash | varchar(64) | NN, UK | SHA-256 del token de invitación. |
| invited_by | uuid | FK → users (CASCADE), NN | Quién envió la invitación. |
| expires_at | timestamptz | NN | Vencimiento (7 días). |
| accepted_at | timestamptz | | Momento de aceptación. |
| accepted_by | uuid | FK → users (SET NULL) | Usuario que aceptó. |
| revoked_at | timestamptz | | Anulación antes de aceptar. |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

### Tabla: `audit_log` — Registro inmutable de auditoría (RNF-14)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del registro de auditoría. |
| actor_user_id | uuid | FK → users (SET NULL) | Quién ejecutó la acción. |
| action | varchar(40) | NN | Verbo del dominio (view_record, dose_log, alert_ack…). |
| entity_type | varchar(40) | NN | Entidad afectada (tabla lógica). |
| entity_id | uuid | | Identificador de la entidad afectada. |
| patient_id | uuid | FK → patients (SET NULL) | Paciente del expediente afectado. |
| old_value | jsonb | | Estado anterior en un cambio (atributos variables). |
| new_value | jsonb | | Estado nuevo en un cambio. |
| ip_address | inet | | IP de origen de la petición. |
| user_agent | varchar(300) | | Agente de la petición. |
| created_at | timestamptz | NN | Momento del evento. |

*Tabla append-only: un trigger impide UPDATE y DELETE (inmutabilidad).*

### Tabla: `system_parameters` — Parámetros de negocio configurables

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| key | varchar(60) | PK | Clave del parámetro (ej. wearable_offline_minutes). |
| value | varchar(120) | NN | Valor del parámetro (como texto). |
| value_type | varchar(20) | NN, def. 'int' | int/minutes/hours/decimal/bool/text. |
| description | varchar(300) | NN | Descripción del parámetro. |
| updated_by | uuid | FK → users (SET NULL) | Último administrador que lo modificó. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

---

## Bloque 2 — Vitals y wearable

### Tabla: `vital_types` — Catálogo de tipos de signos vitales

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| code | varchar(16) | PK | Código del tipo (heart_rate, spo2, …). |
| label | varchar(60) | NN | Nombre legible del signo vital. |
| unit | varchar(10) | NN, def. '' | Unidad de presentación (bpm, %, mmHg…). |
| has_secondary | boolean | NN, def. false | true solo para blood_pressure (sistólica + diastólica). |

### Tabla: `wearables` — Dispositivo vestible vinculado al paciente

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del wearable. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente dueño del dispositivo. |
| provider | varchar(20) | NN, def. 'simulator' | Origen de datos: simulator/healthkit/garmin/… |
| serial_number | varchar(64) | NN | Número de serie del aparato. |
| model | varchar(60) | | Modelo del aparato. |
| battery_pct | smallint | 0–100 | Nivel de batería. NULL si no ha reportado. |
| last_sync_at | timestamptz | | Última medición recibida (base de alerta offline). |
| unlinked_at | timestamptz | | Desvinculación. NULL = vigente. |
| created_at | timestamptz | NN | Vinculación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

*UK parciales: un wearable activo por paciente; un serial activo por proveedor.*

### Tabla: `vital_readings` — Mediciones de signos vitales (particionada por mes)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK (id, measured_at) | Identificador de la lectura. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente al que pertenece. |
| type | varchar(16) | FK → vital_types.code, NN | Tipo de signo vital. |
| value | numeric(8,2) | NN, CHECK 0–100000 | Valor principal (sistólica en presión). |
| value_secondary | numeric(8,2) | solo blood_pressure | Diastólica. NULL en los demás tipos. |
| measured_at | timestamptz | NN, parte de PK | Momento de la medición (columna de particionado). |
| source | varchar(10) | NN | wearable / manual. |
| meta | jsonb | | Datos adicionales del proveedor (atributos variables). |
| created_at | timestamptz | NN | Llegada al servidor. |

*UK natural: (patient_id, type, measured_at, source) → idempotencia.*

### Tabla: `vital_thresholds` — Rango normal por paciente y tipo

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del umbral. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| type | varchar(16) | FK → vital_types.code, NN | Tipo de signo vital. |
| min_value | numeric(8,2) | | Límite inferior. NULL si solo hay techo. |
| max_value | numeric(8,2) | | Límite superior. NULL si solo hay piso. |
| updated_by | uuid | FK → users (SET NULL) | Quién configuró el umbral. |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

*UK: (patient_id, type). CHECK: min < max; al menos uno no nulo.*

### Tabla: `wellbeing_snapshots` — Historial diario del semáforo de bienestar

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del snapshot. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| snapshot_date | date | NN, UK (patient_id, date) | Día de la fotografía. |
| status | varchar(12) | NN | ok / warning / attention. |
| reasons | jsonb | NN, def. '[]' | Motivos legibles del estado (arreglo). |
| vitals_out_of_range | smallint | NN | Conteo de vitales fuera de rango ese día. |
| doses_missed | smallint | NN | Conteo de dosis omitidas ese día. |
| active_alerts | smallint | NN | Conteo de alertas activas ese día. |
| computed_at | timestamptz | NN | Momento del cálculo. |

---

## Bloque 3 — Medicación

### Tabla: `medications` — Plan de medicamento

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del medicamento. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| name | varchar(120) | NN | Nombre del medicamento. |
| dose_amount | numeric(8,2) | NN, CHECK > 0 | Cantidad de la dosis (ej. 50). |
| dose_unit | varchar(20) | NN | Unidad: mg/g/ml/mcg/UI/gotas/… |
| dose_text | varchar(60) | GENERATED | Presentación (cantidad + unidad). Solo lectura. |
| instructions | text | | Instrucciones de administración. |
| start_date | date | NN | Inicio del tratamiento. |
| end_date | date | | Fin del tratamiento. Opcional. |
| grace_window_min | smallint | NN, def. 60 (5–720) | Tolerancia antes de marcar como omitida. |
| prescribed_by | uuid | FK → users (SET NULL) | Médico o cuidadora que definió el plan. |
| discontinued_at | timestamptz | | Descontinuación. NULL = vigente. |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

### Tabla: `medication_times` — Horarios de toma (1FN)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del horario. |
| medication_id | uuid | FK → medications (CASCADE), NN | Medicamento. |
| time_of_day | time | NN, UK (medication_id, time_of_day) | Hora de toma (HH:MM). |

### Tabla: `medication_days` — Días habilitados (1FN)

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| medication_id | uuid | PK (medication_id, day_of_week), FK → medications (CASCADE) | Medicamento. |
| day_of_week | smallint | PK, CHECK 1–7 | 1=lunes … 7=domingo (ISO 8601). |

### Tabla: `scheduled_doses` — Tomas concretas programadas

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la toma. |
| medication_id | uuid | FK → medications (CASCADE), NN | Medicamento del que proviene. |
| scheduled_at | timestamptz | NN, UK (medication_id, scheduled_at) | Cuándo DEBÍA administrarse (planificado). |
| status | varchar(10) | NN, def. 'pending' | pending/taken/skipped/postponed/missed. |
| administered_at | timestamptz | CHECK si taken; ≥ scheduled_at | Cuándo se administró REALMENTE (hecho clínico). |
| logged_by | uuid | FK → users (SET NULL) | Quién registró la toma (responsabilidad). |
| logged_at | timestamptz | | Cuándo se REGISTRÓ en la app (acto administrativo). |
| reason | varchar(200) | obligatorio si skipped | Motivo de la omisión. |
| postponed_until | timestamptz | ≤ scheduled_at + 4h | Nueva hora tras posponer. |
| created_at | timestamptz | NN | Generación de la toma. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

---

## Bloque 4 — Alertas y emergencias

### Tabla: `alerts` — Alertas del sistema

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la alerta. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| type | varchar(20) | NN | fall/vital_out_of_range/missed_dose/sos/wearable_offline. |
| severity | varchar(10) | NN | info / warning / critical. |
| title | varchar(120) | NN | Título de la alerta. |
| detail | text | | Detalle legible. |
| payload | jsonb | | Datos que la originaron (atributos variables). |
| dedup_key | varchar(60) | | Clave de deduplicación (misma causa en 30 min). |
| status | varchar(12) | NN, def. 'active' | active / acknowledged / resolved. |
| acknowledged_by | uuid | FK → users (SET NULL) | Quién atendió. |
| acknowledged_at | timestamptz | | Momento de atención. |
| resolved_by | uuid | FK → users (SET NULL) | Quién resolvió. |
| resolved_at | timestamptz | | Momento de resolución. |
| resolution_note | varchar(500) | | Nota de resolución. |
| escalated_at | timestamptz | | Momento de escalamiento (RF-52). |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

*CHECK: coherencia de estados (no se resuelve antes de atender).*

### Tabla: `alert_deliveries` — Entregas de notificación por alerta

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la entrega. |
| alert_id | uuid | FK → alerts (CASCADE), NN | Alerta notificada. |
| user_id | uuid | FK → users (CASCADE), NN | Destinatario. |
| push_device_id | uuid | FK → push_devices (SET NULL) | Dispositivo al que se envió. |
| channel | varchar(10) | NN, def. 'push' | push/email/sms/in_app. |
| status | varchar(10) | NN, def. 'queued' | queued/sent/delivered/opened/failed. |
| sent_at | timestamptz | | Enviado al proveedor. |
| delivered_at | timestamptz | | Confirmado al dispositivo (mide latencia RNF-05). |
| opened_at | timestamptz | | Abierto por el usuario. |
| error_detail | varchar(300) | obligatorio si failed | Detalle del fallo. |
| created_at | timestamptz | NN | Creación. |

### Tabla: `notification_settings` — Preferencias de notificación

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador. |
| user_id | uuid | FK → users (CASCADE), NN | Usuario. |
| alert_type | varchar(20) | NN, UK (user_id, alert_type) | Tipo de alerta. |
| push_enabled | boolean | NN, def. true | Si recibe push de ese tipo. |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

*CHECK: fall y sos no se pueden desactivar.*

### Tabla: `emergency_contacts` — Contactos de emergencia

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del contacto. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| first_name | varchar(60) | NN | Nombre(s) del contacto. |
| last_name | varchar(60) | NN | Apellido(s) del contacto. |
| full_name | varchar(121) | GENERATED | Nombre completo calculado. Solo lectura. |
| relationship | varchar(40) | | Relación con el paciente. |
| phone | varchar(16) | NN, formato +E.164 | Teléfono de contacto. |
| escalation_order | smallint | NN, def. 1 (1–10) | Prioridad de aviso (1 = primero). |
| notes | varchar(200) | | Notas. |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |
| deleted_at | timestamptz | | Baja lógica. |

### Tabla: `sos_events` — Activaciones del botón de emergencia

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador del evento SOS. |
| patient_id | uuid | FK → patients (CASCADE), NN | Paciente. |
| triggered_by | uuid | FK → users (SET NULL) | Quién activó el SOS. |
| alert_id | uuid | FK → alerts (CASCADE), NN, UK | Alerta crítica generada (una por SOS). |
| note | varchar(300) | | Nota del evento. |
| latitude | numeric(9,6) | −90 a 90 | Latitud al momento del SOS. |
| longitude | numeric(9,6) | −180 a 180 | Longitud al momento del SOS. |
| created_at | timestamptz | NN | Momento del evento. |

---

## Bloque 5 — Negocio (freemium)

### Tabla: `subscriptions` — Suscripciones del modelo freemium

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | uuid | PK | Identificador de la suscripción. |
| user_id | uuid | FK → users (CASCADE), NN | Usuario suscrito (cuidadora en v1). |
| plan | varchar(20) | NN | free / premium. |
| status | varchar(20) | NN, def. 'active' | active/past_due/cancelled/expired. |
| started_at | timestamptz | NN | Inicio de la suscripción. |
| current_period_end | timestamptz | | Fin del período vigente. |
| cancelled_at | timestamptz | obligatorio si cancelled | Momento de cancelación. |
| provider_ref | varchar(120) | | Referencia opaca a la pasarela (sin datos de tarjeta). |
| created_at | timestamptz | NN | Creación. |
| updated_at | timestamptz | NN | Última modificación (trigger). |

*UK parcial: una suscripción activa por usuario.*

---

## Resumen

| Bloque | Tablas | Nº |
|---|---|---|
| 1 · Identidad y acceso | users, refresh_tokens, push_devices, patients, patient_conditions, patient_members, invitations, audit_log, system_parameters | 9 |
| 2 · Vitals y wearable | vital_types, wearables, vital_readings, vital_thresholds, wellbeing_snapshots | 5 |
| 3 · Medicación | medications, medication_times, medication_days, scheduled_doses | 4 |
| 4 · Alertas y emergencias | alerts, alert_deliveries, notification_settings, emergency_contacts, sos_events | 5 |
| 5 · Negocio (freemium) | subscriptions | 1 |
| **Total** | | **24** |
