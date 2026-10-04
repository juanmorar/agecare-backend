# AgeCare — Entregables del 04 de octubre (Avance Fase 2)

**Proyecto APT · Capstone PTY4614 · DUOC UC — Sede San Andrés**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Metodología:** Enfoque Tradicional (Cascada)

Índice de los entregables comprometidos para el 04 de octubre y verificación de que el modelo
de datos soporta lo definido, en honor a la transparencia con la planificación aprobada en
Fase 1 (documento *1.5 — Definición Proyecto APT*).

---

## 1. Contexto en el cronograma (Cascada)

Según la Carta Gantt del documento de Fase 1, el proyecto avanza en etapas secuenciales:

| Fase | Semanas | Etapa de la cascada | Estado |
|---|---|---|---|
| **Fase 1** | S1–S4 | Análisis y Definición de Requisitos + inicio de Diseño | ✅ Aprobada (nota 60/70) |
| **Fase 2** | S5–S16 | Diseño del Sistema → Implementación → Pruebas | 🔄 En curso |
| **Fase 3** | S17–S18 | Empaquetado Docker, Despliegue y Manual Técnico | ⏳ Pendiente |

**La entrega del 04 de octubre es un avance de la Fase 2**: cierra el *Diseño del Sistema*
(modelo de datos definitivo, consolidación de requisitos e historias de usuario) y evidencia el
inicio de la *Implementación* del núcleo de salud. La presentación integral de todo lo
construido ocurre al cierre de la Fase 2.

---

## 2. Entregables del 04 de octubre

| # | Entregable solicitado | Documento | Estado |
|---|---|---|---|
| 1 | Definición de requerimientos | `01_Definicion_Requerimientos_v1.md` | ✅ |
| 2 | Definición de historias de usuario | `02_Historias_de_Usuario_v1.md` | ✅ |
| 3 | Modelo de datos definitivo | `03_Modelo_de_Datos_Definitivo_v1.md` | ✅ |
| 4 | Entregables en base a la planificación | Este índice + matrices de trazabilidad | ✅ |
| — | *(Respaldo)* Análisis de realidad y decisiones de diseño | `04_Analisis_de_Realidad_y_Decisiones.md` | ✅ |
| — | *(Respaldo)* Normalización del modelo (2FN) | `Normalizacion_2FN_AgeCare.md` | ✅ |
| — | *(Respaldo)* Esquema SQL ejecutable (24 tablas) | `sql/*.sql` + `sql/000_schema_completo.sql` | ✅ |
| — | *(Respaldo)* Diagramas ER | `ER_AgeCare.dbml` · `ER_AgeCare_Mermaid.md` | ✅ |
| — | *(Respaldo)* ERS simplificado (Fase 1, fuente de requisitos) | `Documento de Requerimientos (ERS simplificado).md` | ✅ |

---

## 3. Cadena de trazabilidad (sin huecos)

```
ERS simplificado (Fase 1)  ──  RF-01…82 / RNF-01…25     ← fuente de verdad de requisitos
        │
        ▼
01 · Definición de requerimientos   (consolida y traza RF/RNF ↔ objetivos)
        │
        ▼
02 · Historias de usuario           (HU-01…39 derivadas de los RF, con CU-01…07)
        │
        ▼
03 · Modelo de datos definitivo     (24 tablas ↔ RF del ERS)
        │
        ▼
Esquema SQL ejecutable (sql/*.sql) + API FastAPI
        │
        ▼
Carta Gantt del 1.5  (Fase 1 → Fase 2 → Fase 3)
```

---

## 4. Verificación: ¿el modelo soporta lo planificado?

### Núcleo de salud — construido y verificable (avance 04-oct)

| Módulo del ERS | RF | Historias | Tablas | Cobertura |
|---|---|---|---|---|
| Autenticación y cuentas | RF-01…07 | HU-01…05 | `users`, `refresh_tokens`, `push_devices` | ✅ 100% |
| Pacientes y círculo | RF-08…16 | HU-06…11 | `patients`, `patient_conditions`, `patient_members`, `invitations`, `wearables` | ✅ 100% |
| Salud y signos vitales | RF-17…23 | HU-12…16 | `vital_types`, `vital_readings`, `vital_thresholds` | ✅ 100% |
| Medicamentos y adherencia | RF-24…33 | HU-17…22 | `medications`, `medication_times`, `medication_days`, `scheduled_doses` | ✅ 100% (OCR = lógica de app) |
| Alertas y emergencias | RF-44…52 | HU-23…26 | `alerts`, `alert_deliveries`, `notification_settings`, `emergency_contacts`, `sos_events` | ✅ 100% |

**26 historias del núcleo trazadas al ERS y respaldadas por 24 tablas (25 con soporte directo
en el modelo; la digitalización de recetas por OCR, HU-22, es lógica de aplicación sobre las
mismas tablas de medicamentos). Cero requisitos del núcleo sin soporte de datos.**

### Lo que está DECLARADO y pendiente (resto de la Fase 2) — en honor a la transparencia

| Módulo del ERS | RF | Historias | Por qué aún no está |
|---|---|---|---|
| Bitácora del expediente | RF-34…38 | HU-27…29 | Se diseña e implementa más adelante en Fase 2. |
| Archivos y documentos | RF-39…43 | HU-30 | Requiere almacenamiento de archivos (etapa posterior). |
| Comunicación + Asistente IA | RF-53…59 | HU-31, HU-32 | Mensajería y asistente IA, etapa posterior. |
| Vista del adulto mayor (+ Director Musical) | RF-60…69 | HU-33…36 | Depende de servicios de Alloxentric (incluye su configuración Azure). |
| Operación de la cuidadora | RF-70…74 | HU-37 | Perfil profesional, tareas y reportes, etapa posterior. |
| Marketplace | RF-75…79 | HU-38 | Vitrina de cuidadoras y productos, etapa posterior. |
| Funcionamiento sin conexión | RF-80…82 | HU-39 | Capacidad del lado de la aplicación móvil. |

Estos módulos **no requieren rediseñar el núcleo**: se integran con el mismo patrón ya probado
(claves foráneas a `patients`/`users` y control de acceso por `patient_members`). El modelo
definitivo es una base estable, coherente con el avance secuencial de la metodología en cascada.

---

## 5. Decisiones de diseño que respaldan la planificación

1. **Modelo relacional normalizado hasta 2FN** — revisión completa documentada en
   `Normalizacion_2FN_AgeCare.md`: 11 correcciones estructurales + 4 excepciones técnicas
   justificadas. Sin persistencia documental ni NoSQL (todo PostgreSQL).

2. **Análisis de realidad** — el documento `04_Analisis_de_Realidad_y_Decisiones.md` anticipa
   los escenarios del mundo real (wearable apagado, dosis registrada tarde, negligencia humana,
   olvido) y nombra explícitamente el límite entre lo que la tecnología garantiza y lo que
   depende del factor humano. De ahí nacen las tablas `audit_log`, `system_parameters`,
   `wellbeing_snapshots` y `subscriptions`.

3. **Control de acceso centralizado** — `patient_members` es el único punto de verificación de
   permisos, cumpliendo RF-11…14 y RNF-12 sin dispersar la lógica.

4. **Escalabilidad desde el diseño** — `vital_readings` particionada por mes (RNF-07),
   anticipando el volumen de telemetría del wearable.

5. **Trazabilidad clínica inmutable** — `audit_log` registra quién accedió o modificó qué, con
   un trigger que impide alterar o borrar la evidencia (RNF-14).

6. **Catálogo único de tipos y parámetros configurables** — `vital_types` evita duplicar
   definiciones; `system_parameters` saca los umbrales de negocio del código.

---

## 6. Nota sobre las métricas de los objetivos

Los objetivos específicos del documento de Fase 1 incluyen métricas cuantitativas (reducción de
tiempos de respuesta, adherencia, adopción, conversión, latencia y disponibilidad). Estas
métricas se mantienen con **orientación de análisis de negocio**: representan la proyección del
producto en operación real a futuro, no mediciones del alcance académico del APT. Así fueron
avaladas en la revisión de Fase 1.

---

## 7. Resumen ejecutivo para la entrega

> El avance del 04 de octubre cierra el **Diseño del Sistema** de la Fase 2 con el **modelo de
> datos definitivo** (24 tablas en PostgreSQL, normalizado hasta 2FN) que soporta el **100% del
> núcleo de salud** (RF-01…33 y RF-44…52) y las 26 historias de usuario del núcleo, todas
> trazadas al ERS aprobado en Fase 1. El esquema es ejecutable (`sql/*.sql`) y ya está consumido por la API en
> FastAPI. Los módulos restantes del ERS están especificados y declarados, y se completan en el
> resto de la Fase 2 según la Carta Gantt, sin rediseño del núcleo.

**Documentos a presentar el 04 de octubre:**
1. `00_Entregables_04_Octubre_v1.md` (este índice)
2. `01_Definicion_Requerimientos_v1.md`
3. `02_Historias_de_Usuario_v1.md`
4. `03_Modelo_de_Datos_Definitivo_v1.md`
5. `04_Analisis_de_Realidad_y_Decisiones.md` (anticipa preguntas de evaluadores)
6. `Normalizacion_2FN_AgeCare.md` (respaldo del diseño)
7. Diagramas ER: `ER_AgeCare.dbml` / `ER_AgeCare_Mermaid.md`
