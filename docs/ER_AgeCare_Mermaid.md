# AgeCare — Diagrama Entidad-Relación (Mermaid)

**Proyecto APT · Capstone PTY4614 · DUOC UC**
Modelo de datos definitivo · PostgreSQL · 20 tablas · Normalizado hasta 2FN

> Este diagrama se renderiza automáticamente en GitHub y en cualquier visor Markdown con
> soporte Mermaid (VS Code con extensión, Obsidian, etc.). Para exportarlo como imagen se
> puede usar [mermaid.live](https://mermaid.live) pegando el bloque de código.

---

## Diagrama completo

```mermaid
erDiagram
    users ||--o{ refresh_tokens : "tiene"
    users ||--o{ push_devices : "registra"
    users ||--o{ patient_members : "participa"
    users ||--o{ notification_settings : "configura"
    users ||--o{ invitations : "invita"

    patients ||--o{ patient_conditions : "padece"
    patients ||--o{ patient_members : "es cuidado por"
    patients ||--o{ invitations : "recibe"
    patients ||--o{ wearables : "usa"
    patients ||--o{ vital_readings : "genera"
    patients ||--o{ vital_thresholds : "define"
    patients ||--o{ medications : "tiene plan"
    patients ||--o{ alerts : "origina"
    patients ||--o{ emergency_contacts : "tiene"
    patients ||--o{ sos_events : "activa"

    vital_types ||--o{ vital_readings : "clasifica"
    vital_types ||--o{ vital_thresholds : "clasifica"

    medications ||--o{ medication_times : "se toma a"
    medications ||--o{ medication_days : "se toma en"
    medications ||--o{ scheduled_doses : "programa"

    alerts ||--o{ alert_deliveries : "se entrega en"
    alerts ||--|| sos_events : "corresponde a"

    push_devices ||--o{ alert_deliveries : "recibe"

    users {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar first_name
        varchar last_name
        varchar full_name "GENERATED"
        varchar phone
        varchar locale
        boolean is_active
        timestamptz deleted_at
    }

    refresh_tokens {
        uuid id PK
        uuid user_id FK
        uuid family_id
        varchar token_hash UK
        timestamptz expires_at
        timestamptz revoked_at
    }

    push_devices {
        uuid id PK
        uuid user_id FK
        varchar push_token UK
        varchar platform
        boolean is_active
    }

    patients {
        uuid id PK
        varchar first_name
        varchar last_name
        varchar full_name "GENERATED"
        integer rut_number
        char rut_dv
        date birth_date
        char sex
        varchar timezone
        timestamptz deleted_at
    }

    patient_conditions {
        uuid id PK
        uuid patient_id FK
        varchar condition
        date diagnosed_at
    }

    patient_members {
        uuid id PK
        uuid patient_id FK
        uuid user_id FK
        varchar role "family|caregiver|doctor|elder"
        boolean is_owner
        timestamptz removed_at
    }

    invitations {
        uuid id PK
        uuid patient_id FK
        varchar email
        varchar role
        varchar token_hash UK
        uuid invited_by FK
        timestamptz expires_at
        timestamptz accepted_at
        uuid accepted_by FK
    }

    vital_types {
        varchar code PK
        varchar label
        varchar unit
        boolean has_secondary
    }

    wearables {
        uuid id PK
        uuid patient_id FK
        varchar provider
        varchar serial_number
        smallint battery_pct
        timestamptz last_sync_at
        timestamptz unlinked_at
    }

    vital_readings {
        uuid id PK
        timestamptz measured_at PK
        uuid patient_id FK
        varchar type FK
        numeric value
        numeric value_secondary
        varchar source "wearable|manual"
        jsonb meta
    }

    vital_thresholds {
        uuid id PK
        uuid patient_id FK
        varchar type FK
        numeric min_value
        numeric max_value
        uuid updated_by FK
    }

    medications {
        uuid id PK
        uuid patient_id FK
        varchar name
        varchar dose
        text instructions
        date start_date
        date end_date
        smallint grace_window_min
        uuid prescribed_by FK
        timestamptz discontinued_at
    }

    medication_times {
        uuid id PK
        uuid medication_id FK
        time time_of_day
    }

    medication_days {
        uuid medication_id PK_FK
        smallint day_of_week PK "1=lun..7=dom"
    }

    scheduled_doses {
        uuid id PK
        uuid medication_id FK
        timestamptz scheduled_at
        varchar status "pending|taken|skipped|postponed|missed"
        uuid logged_by FK
        timestamptz logged_at
        varchar reason
        timestamptz postponed_until
    }

    alerts {
        uuid id PK
        uuid patient_id FK
        varchar type "fall|vital_out_of_range|missed_dose|sos|wearable_offline"
        varchar severity "info|warning|critical"
        varchar title
        jsonb payload
        varchar dedup_key
        varchar status "active|acknowledged|resolved"
        uuid acknowledged_by FK
        uuid resolved_by FK
        timestamptz escalated_at
    }

    alert_deliveries {
        uuid id PK
        uuid alert_id FK
        uuid user_id FK
        uuid push_device_id FK
        varchar channel
        varchar status
        timestamptz sent_at
        timestamptz delivered_at
        timestamptz opened_at
    }

    notification_settings {
        uuid id PK
        uuid user_id FK
        varchar alert_type
        boolean push_enabled
    }

    emergency_contacts {
        uuid id PK
        uuid patient_id FK
        varchar full_name
        varchar relationship
        varchar phone
        smallint escalation_order
        timestamptz deleted_at
    }

    sos_events {
        uuid id PK
        uuid patient_id FK
        uuid triggered_by FK
        uuid alert_id FK "UK"
        varchar note
        numeric latitude
        numeric longitude
    }
```

---

## Lectura rápida por bloques

| Bloque | Tablas | Relación clave |
|---|---|---|
| **Identidad y acceso** | users, refresh_tokens, push_devices, patients, patient_conditions, patient_members, invitations | `patient_members` conecta `users` ↔ `patients` (control de acceso) |
| **Vitals y wearable** | vital_types, wearables, vital_readings, vital_thresholds | `vital_types` es catálogo referenciado por lecturas y umbrales |
| **Medicación** | medications, medication_times, medication_days, scheduled_doses | `medications` 1:N horarios/días; genera `scheduled_doses` |
| **Alertas y emergencias** | alerts, alert_deliveries, notification_settings, emergency_contacts, sos_events | `alerts` 1:1 `sos_events`; 1:N `alert_deliveries` |

**Notación:** `PK` clave primaria · `FK` clave foránea · `UK` único ·
`||--o{` uno a muchos · `||--||` uno a uno.
