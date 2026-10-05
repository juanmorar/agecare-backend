# Guía 2. Desarrollo Proyecto APT — Informe de Avance (Fase 2)

**Asignatura:** Capstone · PTY4614
**Proyecto:** AgeCare — Plataforma digital integral de cuidado de adultos mayores
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Carrera:** Ingeniería en Informática · **Sede:** San Andrés
**Metodología:** Enfoque Tradicional (Cascada)
**Repositorio:** https://github.com/juanmorar/agecare-backend
**API desplegada (evidencia en vivo):** https://agecare-api.javiercerna.dev/docs

---

## 1. Resumen de avance del Proyecto APT

Durante esta fase el equipo ejecutó las etapas de **Análisis y Definición de Requisitos** y
**Diseño del Sistema** del plan en cascada, y dio inicio a la **Implementación**.

**Alcance del proyecto y su doble contexto.** El Proyecto APT se desarrolla como una **solución
full stack** completa (backend en FastAPI + base de datos PostgreSQL + aplicación móvil en
Flutter con las vistas de los tres roles), tal como lo exige el perfil de egreso y lo refleja el
cronograma en cascada de la Fase 1 (etapas de backend en S7–S11 y de frontend móvil en S12–S14).
Este alcance full stack es el que se entrega y evalúa en el marco académico de DUOC UC.

En paralelo, el equipo colabora con la empresa **Alloxentric** —de la cual proviene la
especificación funcional del producto—, aportando principalmente el desarrollo del **backend y
la base de datos** que dan servicio a todos los roles. Esta relación con una contraparte real es
la que justifica dos decisiones de Fase 1: el uso de una **metodología en cascada** (los
requisitos llegan estables y documentados desde la empresa) y el **cronograma secuencial** que
primero asienta el núcleo de datos y backend, y luego construye la capa de presentación.

El avance de esta fecha se concentra, por tanto, en las capas de **datos y backend** —la base
sobre la que se levantará el frontend en las etapas siguientes del cronograma—, sin que ello
reduzca el alcance full stack comprometido para el cierre del proyecto.

Concretamente, se completaron las siguientes actividades:

- **Levantamiento y consolidación de requisitos (ERS simplificado):** se formalizaron 82
  requisitos funcionales (RF-01 a RF-82) y 25 requisitos no funcionales (RNF-01 a RNF-25),
  además de 7 casos de uso. Este documento es el contrato de alcance del proyecto.
- **Diseño del modelo de datos definitivo:** se diseñó e implementó en PostgreSQL un modelo
  relacional normalizado hasta la Segunda Forma Normal (2FN), compuesto por 24 tablas, con
  integridad referencial completa, restricciones de dominio (CHECK), índices, triggers y
  particionamiento por tiempo para la telemetría de signos vitales.
- **Implementación del núcleo de salud (backend):** se desarrolló la API REST en FastAPI con
  los módulos de autenticación, pacientes y círculo de cuidado, signos vitales y semáforo,
  medicamentos y adherencia, y alertas/emergencias.
- **Despliegue en infraestructura real:** la API se encuentra publicada y accesible mediante un
  dominio propio con túnel Cloudflare y documentación interactiva (OpenAPI/Swagger).
- **Análisis de realidad y endurecimiento del modelo:** se realizó una revisión de ingeniería
  que anticipa escenarios del mundo real (fallo del wearable, registro tardío de dosis,
  trazabilidad de responsabilidad), incorporando tablas de auditoría, parámetros de sistema,
  historización del bienestar y soporte del modelo freemium.

**Objetivos específicos cumplidos a la fecha** (según los definidos en Fase 1, basados en el
ERS de Alloxentric):

| Objetivo específico                                          | Estado                     | Evidencia                                                                                  |
| ------------------------------------------------------------ | -------------------------- | ------------------------------------------------------------------------------------------ |
| OE-1 Expediente único y semáforo de bienestar multi-paciente | ✅ Núcleo cubierto          | Tablas `patients`, `vital_readings`, `wellbeing_snapshots`; endpoints de vitals y semáforo |
| OE-2 Alertas en tiempo real y botón de emergencia            | ✅ Cubierto                 | Módulo 9 (alertas, SOS), tablas `alerts`, `alert_deliveries`, `sos_events`                 |
| OE-3 Ciclo completo de medicación y adherencia               | ✅ Cubierto (OCR pendiente) | Módulo 6, tablas `medications`, `scheduled_doses`                                          |
| OE-4 Comunicación y asistente IA                             | ⏳ Fase 2 (etapa posterior) | Declarado y trazado en el ERS                                                              |
| OE-5 Experiencia del adulto mayor (incl. Director Musical)   | ⏳ Fase 2 (etapa posterior) | Declarado; depende de servicios de Alloxentric                                             |

El avance se concentró en el **núcleo de salud** (RF-01 a RF-33 y RF-44 a RF-52), que es la
prioridad del proyecto y la base sobre la cual se construyen los módulos restantes.

### Objetivos (ajuste)

No se realizaron ajustes a los objetivos definidos en la Fase 1. Los objetivos general y
específicos se mantienen íntegros, ya que el alcance provino de una especificación estable
entregada por la contraparte. **Se conserva la decisión de Fase 1** de documentar las métricas
cuantitativas de los objetivos (reducción de tiempos de respuesta, adherencia, adopción,
conversión y disponibilidad) con **orientación de análisis de negocio**: representan la
proyección del producto en operación real a futuro, no métricas medibles dentro del alcance
académico del proyecto de título.

### Metodología (ajuste)

No se realizaron ajustes a la metodología. Se mantiene el **Enfoque Tradicional (Cascada)**
definido en Fase 1, con sus cinco etapas secuenciales (Análisis → Diseño → Implementación →
Pruebas → Despliegue). La naturaleza del proyecto —requisitos estables y documentación rigurosa
exigida académicamente— sigue justificando este enfoque. Internamente, y de forma transparente,
el equipo coordina sus entregas con la empresa en ciclos cortos; sin embargo, el marco formal de
titulación y de este informe es Cascada, y así se reporta el avance.

> **Nota de corrección respecto a Fase 1:** en la Guía 1 se describió la persistencia como
> "híbrida / relacional y documental". Tras el diseño definitivo se corrigió esa descripción:
> el modelo es **íntegramente relacional en PostgreSQL, normalizado hasta 2FN**. Los pocos
> campos `jsonb` presentes corresponden a atributos de estructura variable y están documentados
> como excepción justificada. Esta corrección se detalla en el apartado 3.

---

### Evidencias de avance

Las evidencias de esta fase están **todas versionadas en Git** y, en el caso de la API,
desplegadas y accesibles públicamente. Cada evidencia se eligió por dar cuenta verificable de
una etapa del plan en cascada.

| #   | Evidencia                                 | Ubicación                                                | Qué demuestra                                                             |
| --- | ----------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| E1  | **Documento de Requerimientos (ERS)**     | `docs/Documento de Requerimientos (ERS simplificado).md` | Etapa de Análisis: 82 RF, 25 RNF, 7 casos de uso. Contrato de alcance.    |
| E2  | **Modelo de datos definitivo**            | `docs/03_Modelo_de_Datos_Definitivo_v1.md` + `sql/*.sql` | Etapa de Diseño: 24 tablas, 2FN, integridad referencial.                  |
| E3  | **Script SQL ejecutable**                 | `sql/schema/000_schema_completo.sql` + 22 scripts numerados     | Implementación verificable de la BD; reconstruible desde cero.            |
| E4  | **Diagramas Entidad-Relación**            | `docs/ER_AgeCare.dbml` · `docs/ER_AgeCare_Mermaid.md`    | Diseño visual del modelo (dbdiagram.io y Mermaid).                        |
| E5  | **API REST desplegada**                   | https://agecare-api.javiercerna.dev/docs                 | Implementación del backend operando en infraestructura real.              |
| E6  | **Documento de normalización 2FN**        | `docs/Normalizacion_2FN_AgeCare.md`                      | Rigor de diseño: 15 hallazgos, 11 corregidos, 4 excepciones justificadas. |
| E7  | **Análisis de realidad y decisiones**     | `docs/04_Analisis_de_Realidad_y_Decisiones.md`           | Madurez de ingeniería: escenarios del mundo real y decisiones de diseño.  |
| E8  | **Historias de usuario y requerimientos** | `docs/01_...md`, `docs/02_...md`                         | Trazabilidad ERS → RF → historias → tablas.                               |
| E9  | **Historial de commits (Git)**            | `git log` del repositorio                                | Trazabilidad temporal y autoría del trabajo del equipo.                   |

**Justificación de la pertinencia de las evidencias.** Las evidencias cubren las tres
dimensiones que exige la asignatura: **documentación** (E1, E2, E6, E7, E8), **programación**
(E3, E5) y **almacenamiento de datos** (E2, E3, E4). El modelo de datos y su script ejecutable
son el entregable central comprometido para esta fecha de avance, coherente con la etapa de
Diseño del cronograma.

**Resguardo de la calidad desde la disciplina.** La calidad se aseguró con prácticas estándar de
la industria del desarrollo de software y de la ingeniería de datos:

- **Normalización formal hasta 2FN**, con un documento que audita cada decisión y justifica las
  excepciones técnicas (particionamiento, atributos variables).
- **Integridad referencial** garantizada por claves foráneas con política explícita
  (`ON DELETE CASCADE` / `SET NULL`) e **integridad de dominio** mediante restricciones `CHECK`.
- **Control de versiones Git** con commits atómicos y descriptivos por módulo, lo que permite
  trazar la evolución y la autoría.
- **Contenerización con Docker** (`docker-compose.yml`) y **configuración por variables de
  entorno**, cumpliendo portabilidad y separación de secretos.
- **Documentación de la API autogenerada** desde el código (OpenAPI/Swagger), accesible en línea.
- **Seguridad por diseño:** contraseñas con hash, tokens hasheados, control de acceso por rol y
  trazabilidad clínica inmutable (`audit_log`).

---

## 2. Monitoreo del Plan de Trabajo

Se reporta el estado de avance de cada actividad del plan de trabajo definido en la Fase 1,
respetando sus etapas, duraciones y responsables. Estados posibles: *En curso · Con retraso ·
No iniciado · Completado · Ajustada*.

| Competencia / Unidad | Actividad (según Fase 1) | Recursos | Duración | Responsable | Observaciones | Estado de avance | Ajustes |
|---|---|---|---|---|---|---|---|
| Gestión de Proyectos Informáticos | **S1–S3:** Análisis y definición de requisitos (ERS simplificado) y consolidación de requisitos no funcionales | Plantillas ERS, documentación de Alloxentric | 3 semanas | Equipo completo | *Facilitador:* la especificación de Alloxentric ya estaba definida y estable | **Completado** | Sin ajustes |
| Sistematización y Modelos de Datos | **S4–S6:** Diseño de arquitectura y base de datos (modelo ER en PostgreSQL y diagramación) | DBDesigner, dbdiagram.io, Azure | 3 semanas | Benjamín Camus, Juan Mora | *Facilitador:* roles especializados en datos. Se profundizó con normalización 2FN formal | **Completado** | Se agregó documento de normalización y análisis de realidad (mejora de calidad no prevista en Fase 1) |
| Desarrollo de Solución de Software | **S7–S11:** Implementación backend y Core API (FastAPI, integración IA, simulador wearable) | Python, FastAPI, Azure | 5 semanas | Javier Cerna | *Facilitador:* contrato de endpoints definido. Foco en seguridad y control de acceso (JWT) | **En curso** | Núcleo de salud (módulos 3, 4, 5, 6, 9) completado; IA y OCR en etapa posterior |
| Desarrollo de Solución de Software | **S12–S14:** Implementación frontend móvil (Flutter, módulo Director Musical) | Flutter, Dart | 3 semanas | Equipo completo | El módulo Director Musical depende de servicios de Alloxentric | **No iniciado** | Planificado según cronograma; sin adelanto |
| Pruebas de Certificación | **S15–S16:** Pruebas y certificación (seguridad, integración y carga) | Postman, PyTest | 2 semanas | Equipo completo | Paso obligatorio previo al despliegue final | **No iniciado** | Planificado; se dispone de cliente de prueba HTML para validación manual temprana |
| Gestión y Sistematización | **S17–S18:** Empaquetado Docker y despliegue + Manual Técnico | Docker, Azure Container Apps | 2 semanas | Javier Cerna | *Facilitador:* ya existe `docker-compose` y despliegue anticipado de la API | **En curso (adelantado)** | La API ya está contenerizada y desplegada antes de lo planificado; evidencia disponible en vivo |

**Resumen del estado:** las actividades de Análisis y Diseño (S1–S6) están **completadas**; la
Implementación del backend (S7–S11) está **en curso** con el núcleo de salud operativo; el
empaquetado y despliegue (S17–S18) se **adelantó** parcialmente al disponer ya de la API
contenerizada y publicada. Las etapas de **frontend móvil en Flutter (S12–S14)** —parte del
alcance full stack comprometido para DUOC— y las **pruebas formales (S15–S16)** siguen el
calendario de la cascada y se abordan una vez consolidada la capa de datos y backend, respetando
la secuencialidad del método.

---

## 3. Ajustes a partir del monitoreo

### Factores que han facilitado y/o dificultado el desarrollo

**Facilitadores:**

- **Especificación estable desde la contraparte (Alloxentric):** contar con el ERS y la
  especificación de endpoints ya definidos eliminó la incertidumbre de alcance y permitió que
  el equipo se concentrara en el diseño y la construcción. Esto es coherente con el enfoque
  Cascada, que requiere requisitos estables al inicio.
- **Roles especializados y complementarios:** la distribución DBA (Juan Mora) / Arquitecto de
  Datos (Benjamín Camus) / Full Stack y DevSecOps (Javier Cerna) permitió avanzar en paralelo en
  el modelado de datos y el backend, y cubre las competencias necesarias para completar la
  solución full stack (incluida la capa móvil en Flutter) en las etapas siguientes.
- **Despliegue temprano:** disponer de la API en un dominio propio con túnel Cloudflare dio una
  evidencia tangible y verificable del avance, y adelantó parte de la etapa de despliegue.

**Dificultades y cómo se abordaron:**

- **Curva de diseño en la nube (Cloud):** señalada como obstaculizador en la Fase 1. Se abordó
  usando contenedores Docker, lo que estandarizó el entorno y redujo la fricción de despliegue.
- **Integración con hardware real del wearable:** riesgo identificado en Fase 1. Se mitigó con
  un **simulador de ingesta de datos** desacoplado por la API de ingesta batch, evitando el
  bloqueo técnico, tal como se había previsto como solución en la Factibilidad del proyecto.
- **Rigor de normalización:** al revisar el modelo contra las formas normales se detectaron
  oportunidades de mejora (arreglos JSON, dependencias parciales, un typo que inutilizaba un
  trigger). Se corrigieron y documentaron antes de avanzar, elevando la calidad del diseño.

### Actividades ajustadas o eliminadas

No se eliminaron actividades. Se realizaron dos **mejoras de calidad no previstas** en la Fase 1,
que fortalecen el proyecto sin alterar su alcance:

1. **Normalización formal a 2FN con documento de respaldo** (`Normalizacion_2FN_AgeCare.md`):
   se corrigió el modelo donde había arreglos JSON multivaluados, una dependencia parcial y
   duplicación de catálogos, y se documentaron las excepciones técnicas justificadas.
2. **Análisis de realidad** (`04_Analisis_de_Realidad_y_Decisiones.md`): se incorporaron cuatro
   tablas transversales (`audit_log`, `system_parameters`, `wellbeing_snapshots`,
   `subscriptions`) que responden a escenarios del mundo real y a requisitos no funcionales
   (trazabilidad clínica, configurabilidad, historización, modelo freemium).

Adicionalmente, se corrigió la descripción de la persistencia de datos respecto de la Fase 1
(de "híbrida/documental" a "relacional normalizada en PostgreSQL"), para que la documentación
refleje fielmente el modelo construido. Este es el único ajuste de redacción respecto del
documento de Fase 1, y se deja constancia explícita de él en honor a la trazabilidad.

### Actividades no iniciadas o retrasadas

- **Frontend móvil en Flutter (S12–S14):** no iniciado. Corresponde a una etapa posterior del
  cronograma en cascada; su no inicio es conforme a lo planificado, no un retraso. Para la
  validación temprana del backend se dispone de un cliente de prueba HTML servido por la propia
  API (`/test`), que permite ejercitar los endpoints sin esperar la app.
- **Módulos de comunicación, asistente IA y vista del adulto mayor (incl. Director Musical):**
  no iniciados; declarados y trazados en el ERS para las etapas siguientes. El módulo Director
  Musical, en particular, depende de servicios y credenciales que administra Alloxentric.
- **Pruebas de certificación formales (S15–S16):** no iniciadas, conforme al calendario.

### Pendiente de consolidación en el repositorio

Se deja constancia de que la **evidencia de aporte en Git del integrante Benjamín Camus**
(responsable del modelado y la arquitectura de datos junto a Juan Mora) se encuentra en proceso
de consolidación: sus contribuciones de diseño serán incorporadas como commits con su autoría
antes del cierre de la evaluación, de modo que el historial del repositorio refleje de forma
equitativa la participación de los tres integrantes. A la fecha de este informe, el historial
registra la autoría de Javier Cerna y Juan Mora; la de Benjamín Camus se incorporará en los días
siguientes.

---

## 4. Síntesis de congruencia con la Fase 1

El avance reportado es **congruente con la Definición del Proyecto (Fase 1)**:

- **Objetivos:** se mantienen sin cambios; el avance cumple OE-1, OE-2 y OE-3 en su núcleo.
- **Metodología:** se mantiene Cascada; el avance corresponde a las etapas de Análisis, Diseño
  e inicio de Implementación.
- **Alcance:** se mantiene la solución **full stack** comprometida para DUOC (backend + base de
  datos + app móvil Flutter). El avance de esta fecha cubre las capas de datos y backend; la
  capa de presentación corresponde a las etapas S12–S14 del cronograma, aún no iniciadas por
  secuencialidad de la cascada.
- **Plan de trabajo:** las actividades S1–S6 están completadas y S7–S11 en curso, según el
  cronograma; el despliegue (S17–S18) se adelantó parcialmente.
- **Evidencias:** coinciden con las comprometidas en Fase 1 (Documento de Requerimientos y
  Arquitectura, Modelo de datos, Docker), más mejoras de calidad documentadas.
- **Única corrección de redacción:** la descripción de la persistencia, ajustada a la realidad
  del modelo relacional, declarada explícitamente en este informe.
