**AgeCare**

Plataforma de cuidado de adultos mayores

Documento de Diseño

Capstone · PTY4614 · Portafolio de Título

Jazna Patricia Meza Hidalgo \| Juan Pablo Mellado Alarcon

Javier Cerna · Juan Mora · Benja Camus

**Índice**

[1. Introducción 3](#_heading=)

[2. Arquitectura del sistema 3](#_heading=)

> [2.1 Visión general 3](#_heading=)
>
> [2.2 Componentes 4](#_heading=)
>
> [2.3 Comunicación entre servicios 4](#_heading=)
>
> [2.4 Tecnologías 4](#_heading=)

[3. Modelo de datos 5](#_heading=)

> [3.1 Enfoque 5](#_heading=)
>
> [3.2 Núcleo: identidad, pacientes y signos vitales 5](#_heading=)
>
> [3.3 Expediente clínico: medicación, bitácora y alertas 7](#_heading=)
>
> [3.4 Comunicación y acompañamiento 8](#_heading=)
>
> [3.5 Organización de las tablas 9](#_heading=)
>
> [3.6 Decisiones de diseño 9](#_heading=)

[4. Diagramas UML 10](#_heading=)

> [4.1 Diagrama de casos de uso 10](#_heading=)
>
> [4.2 Diagrama de clases 10](#_heading=)
>
> [4.3 Diagrama de secuencia 12](#_heading=)
>
> [4.4 Diagrama de componentes 12](#_heading=)

[5. Diseño de despliegue con Docker 13](#_heading=)

> [5.1 Contenedores 13](#_heading=)
>
> [5.2 Dockerfile 13](#_heading=)
>
> [5.3 docker-compose.yml 13](#_heading=)
>
> [5.4 Variables de entorno 14](#_heading=)
>
> [5.5 Cómo levantar el sistema 14](#_heading=)

# **1. Introducción** {#introducción}

Este documento describe cómo está construido AgeCare por dentro: la arquitectura del sistema, el modelo de datos, los diagramas que representan su comportamiento y la forma en que se despliega mediante contenedores.

Complementa al Documento de Requerimientos, que define qué debe hacer el sistema. Aquí se explica cómo se resuelve. Cada decisión de diseño que aparece a continuación responde a uno o más requisitos de ese documento.

# **2. Arquitectura del sistema** {#arquitectura-del-sistema}

## **2.1 Visión general** {#visión-general}

AgeCare se organiza en cuatro capas. La capa de presentación reúne las aplicaciones con las que interactúan los usuarios. La capa de servicios concentra toda la lógica de negocio y es la única que accede a los datos. La capa de datos almacena la información de forma permanente. Los servicios externos aportan capacidades que el sistema no implementa por sí mismo.

La regla que ordena el diseño es simple: ninguna aplicación cliente accede directamente a la base de datos ni a los servicios externos. Todo pasa por el backend, que es donde se validan los permisos. Esto permite que la aplicación móvil, la web y cualquier cliente futuro compartan las mismas reglas sin duplicarlas.

![](media/image7.png){width="6.692716535433071in" height="5.458333333333333in"}

*Figura 1. Arquitectura general del sistema.*

## **2.2 Componentes** {#componentes}

| **Componente** | **Responsabilidad** |
|:---|----|
| App móvil Flutter | Punto de acceso principal para los cuatro roles. Captura datos, muestra el expediente y recibe las notificaciones. Incorpora la vista accesible del adulto mayor. |
| Base de datos local (Drift) | Copia local sobre SQLite que permite consultar y registrar información cuando el dispositivo no tiene conexión, y sincronizarla al recuperarla. |
| Aplicación web (React) | Acceso desde navegador para familiar, cuidadora y médico. Consume la misma API que la aplicación móvil. |
| API REST (FastAPI) | Expone las operaciones del sistema, valida las entradas y aplica el control de acceso por rol antes de tocar los datos. |
| Canal en tiempo real (WebSocket) | Entrega inmediata de los mensajes del chat a los participantes conectados. |
| Motor de alertas | Evalúa las mediciones recibidas, las tomas vencidas y los incidentes, y decide cuándo generar una alerta y a quién notificar. |
| Procesos programados (Worker) | Tareas que se ejecutan sin intervención del usuario: generar las tomas del día, marcar las vencidas y detectar wearables sin datos. |
| PostgreSQL | Almacenamiento principal de toda la información estructurada del sistema. |
| Almacenamiento de archivos | Guarda imágenes, documentos y notas de voz. La aplicación sube y descarga mediante enlaces temporales, sin manejar credenciales. |

## **2.3 Comunicación entre servicios** {#comunicación-entre-servicios}

| **Origen** | **Destino** | **Mecanismo** |
|:---|----|----|
| Aplicaciones cliente | API REST | HTTPS con token de sesión en cada petición. Formato JSON. |
| App móvil | Canal en tiempo real | WebSocket sobre TLS, autenticado con el mismo token de sesión. |
| Backend | PostgreSQL | Conexión interna dentro de la red privada, mediante un conjunto reutilizable de conexiones. |
| Wearables | API REST | El proveedor entrega las mediciones estandarizadas al backend, que las procesa en lotes. |
| Motor de alertas | Servicio de notificaciones | Llamada al proveedor de notificaciones push para entregar el aviso al teléfono. |
| Backend | Modelo de lenguaje | Llamada con el contexto del expediente filtrado según el rol del usuario que pregunta. |
| App móvil | Base de datos local | Acceso directo en el dispositivo, con sincronización posterior contra la API. |

## **2.4 Tecnologías** {#tecnologías}

| **Capa** | **Tecnología** | **Motivo de la elección** |
|:---|----|----|
| Base de datos | PostgreSQL | Permite resolver en un solo motor las dos naturalezas de datos del sistema: información relacional con reglas estrictas y series temporales de alto volumen, mediante particionamiento nativo. |
| Backend | FastAPI (Python) | Validación automática de los datos de entrada y salida, documentación generada desde el código y soporte nativo para operaciones concurrentes y WebSocket. |
| App móvil | Flutter | Una sola base de código para iOS y Android, con acceso a los sensores y a los servicios de salud de cada plataforma. |
| BD local | Drift (SQLite) | Permite consultas relacionales dentro del dispositivo y hace posible el funcionamiento sin conexión. |
| Aplicación web | React | Ecosistema maduro para interfaces con actualización frecuente de datos. |
| Modelo de lenguaje | DeepSeek | Resuelve el asistente sobre el expediente con un costo por consulta acotado. |
| Despliegue | Docker | Reproduce el mismo entorno en los computadores del equipo y en el servidor, sin diferencias de configuración. |

# **3. Modelo de datos** {#modelo-de-datos}

## **3.1 Enfoque** {#enfoque}

El modelo es relacional y se implementa sobre PostgreSQL. Todas las tablas usan un identificador único universal como clave primaria y registran la fecha de creación y de última modificación. En los recursos del expediente clínico el borrado es lógico: el registro se marca como eliminado en lugar de desaparecer, porque la información clínica debe poder auditarse aunque el usuario la haya dado de baja.

Toda la información clínica cuelga del paciente, y el acceso se resuelve consultando la tabla de membresías, que indica qué rol tiene cada usuario sobre cada paciente. Esa tabla es el centro del control de acceso: ninguna consulta al expediente se ejecuta sin verificarla primero.

El modelo se presenta en tres diagramas para mantenerlo legible: el núcleo de identidad y salud, el expediente clínico, y los módulos de comunicación y acompañamiento.

## **3.2 Núcleo: identidad, pacientes y signos vitales** {#núcleo-identidad-pacientes-y-signos-vitales}

![](media/image8.png){width="5.704683945756781in" height="5.773770778652668in"}

*Figura 2. Modelo entidad-relación del núcleo del sistema.*

Un usuario puede estar asociado a varios pacientes y un paciente puede tener varios usuarios a su cargo, cada uno con un rol distinto. Esa relación se resuelve en la tabla de membresías, que además marca quién es el administrador del paciente. Un paciente admite un solo wearable activo, y todas las mediciones quedan asociadas tanto al paciente como a su origen, para distinguir las automáticas de las registradas a mano.

## **3.3 Expediente clínico: medicación, bitácora y alertas** {#expediente-clínico-medicación-bitácora-y-alertas}

![](media/image3.png){width="6.187426727909012in" height="9.69687445319335in"}

*Figura 3. Modelo entidad-relación del expediente clínico.*

El plan de medicamentos y las tomas programadas se modelan por separado. El medicamento define qué se administra y con qué frecuencia; las tomas son las instancias concretas que se generan cada día y que la cuidadora confirma. Esta separación permite responder no solo qué se administró, sino también qué debió administrarse y no se hizo, que es el dato que interesa al familiar.

## **3.4 Comunicación y acompañamiento** {#comunicación-y-acompañamiento}

![](media/image6.png){width="6.692716535433071in" height="7.513888888888889in"}

*Figura 4. Modelo entidad-relación de comunicación y módulos del adulto mayor.*

El chat es único por paciente y admite mensajes de texto, voz y fotografía. El puntero de lectura por usuario permite calcular los mensajes no leídos sin recorrer toda la conversación. Las creaciones musicales incluyen una clave generada en el dispositivo, que evita duplicarlas cuando la sincronización se reintenta tras una pérdida de conexión.

## **3.5 Organización de las tablas** {#organización-de-las-tablas}

| **Módulo** | **Tablas** |
|:---|----|
| Identidad y acceso | users, refresh_tokens, push_devices, patient_members, invitations |
| Pacientes y dispositivos | patients, wearables |
| Signos vitales | vital_readings, vital_thresholds |
| Medicación | medications, scheduled_doses |
| Bitácora del expediente | observations, incidents, handover_notes, elder_checkins |
| Archivos | uploads, documents |
| Alertas y emergencias | alerts, notification_settings, sos_events, alert_deliveries |
| Comunicación | chat_messages, chat_read_pointers, assistant_conversations, assistant_messages |
| Vista del adulto mayor | photos, photo_reactions, content_items, music_sessions, music_songs, share_links, device_link_codes |
| Operación de la cuidadora | care_tasks, caregiver_profiles, caregiver_subscriptions |
| Marketplace | marketplace_products, caregiver_reviews, contact_requests, job_offers |
| Auditoría | clinical_access_log |

## **3.6 Decisiones de diseño** {#decisiones-de-diseño}

Las siguientes decisiones responden directamente a los requisitos no funcionales de rendimiento, escalabilidad y seguridad.

- Particionamiento por mes de la tabla de mediciones. Un solo wearable puede generar decenas de miles de registros diarios. Dividir la tabla por mes mantiene acotado el volumen que recorre cada consulta de tendencias y permite archivar los periodos antiguos sin afectar al resto.

- Ingesta repetible. Una restricción de unicidad sobre paciente, tipo de medición, momento y origen impide que un lote reenviado genere registros duplicados. El sistema descarta las repetidas en silencio en lugar de rechazar el lote completo.

- Índices orientados a las consultas reales. Se definen sobre las cuatro consultas más frecuentes: la serie de mediciones de un paciente, las tomas pendientes por vencer, las alertas activas y el historial del chat.

- Separación entre plan y ejecución. Los medicamentos definen el tratamiento y las tomas registran su cumplimiento. Modificar un medicamento regenera solo las tomas futuras y deja intacto el historial.

- Borrado lógico en el expediente. Los documentos y registros clínicos se marcan como eliminados y el archivo asociado se depura después, para no perder la trazabilidad de lo que existió.

- Registro de accesos clínicos. Una tabla independiente guarda qué usuario consultó qué expediente y cuándo, sin la cual no es posible auditar el uso de información sensible.

- Base de datos local y sincronización. El dispositivo mantiene una copia de la información necesaria para operar sin conexión. Cada registro creado localmente lleva una clave propia, que el servidor usa para reconocerlo si la sincronización se reintenta.

# **4. Diagramas UML** {#diagramas-uml}

## **4.1 Diagrama de casos de uso** {#diagrama-de-casos-de-uso}

Representa las funcionalidades principales del sistema y qué actor las inicia. Cada caso de uso se detalla en el Documento de Requerimientos.

![](media/image2.png){width="4.604166666666667in" height="7.104166666666667in"}

*Figura 5. Diagrama de casos de uso.*

## **4.2 Diagrama de clases** {#diagrama-de-clases}

Muestra las entidades del dominio, sus atributos principales y las operaciones que definen su comportamiento. No representa las tablas de la base de datos, sino los conceptos con que trabaja la lógica de negocio.

![](media/image4.png){width="6.692716535433071in" height="6.319444444444445in"}

*Figura 6. Diagrama de clases del dominio.*

## **4.3 Diagrama de secuencia** {#diagrama-de-secuencia}

Describe la funcionalidad más crítica del sistema: la detección de una caída y el aviso al familiar. Incluye las dos condiciones que evitan un mal funcionamiento conocido: no generar alertas duplicadas por la misma causa y escalar el aviso cuando nadie responde.

![](media/image9.png){width="6.692716535433071in" height="3.4722222222222223in"}

*Figura 7. Secuencia de detección de una caída y notificación al familiar.*

## **4.4 Diagrama de componentes** {#diagrama-de-componentes}

Muestra la organización interna del backend. Los módulos funcionales no acceden a la base de datos directamente: pasan por el control de acceso por rol y por la capa de acceso a datos, lo que garantiza que la validación de permisos no pueda saltarse desde ningún punto.

![](media/image1.png){width="6.692716535433071in" height="2.3055555555555554in"}

*Figura 8. Componentes internos del backend.*

# **5. Diseño de despliegue con Docker** {#diseño-de-despliegue-con-docker}

El sistema se ejecuta en contenedores, de modo que el entorno sea idéntico en los computadores del equipo y en el servidor. Levantar el sistema completo requiere un solo comando y no depende de que cada integrante instale las mismas versiones en su máquina.

![](media/image10.png){width="6.692716535433071in" height="3.5694444444444446in"}

*Figura 9. Contenedores y su comunicación.*

## **5.1 Contenedores** {#contenedores}

| **Contenedor** | **Imagen base** | **Función** |
|:---|----|----|
| db | postgres:16-alpine | Base de datos principal. Los datos persisten en un volumen para que no se pierdan al reiniciar el contenedor. |
| migrations | Imagen del proyecto | Aplica las migraciones pendientes al iniciar y termina. Garantiza que la estructura esté actualizada antes de que arranque la API. |
| api | Imagen del proyecto | Servidor FastAPI. Es el único contenedor expuesto hacia afuera. |
| worker | Imagen del proyecto | Ejecuta los procesos programados: generación de tomas, control de vencimientos y vigilancia del wearable. |

## **5.2 Dockerfile** {#dockerfile}

> FROM python:3.12-slim
>
> ENV PYTHONDONTWRITEBYTECODE=1 \\
>
> PYTHONUNBUFFERED=1
>
> WORKDIR /app
>
> RUN apt-get update && apt-get install -y \--no-install-recommends \\
>
> build-essential libpq-dev && rm -rf /var/lib/apt/lists/\*
>
> COPY requirements.txt .
>
> RUN pip install \--no-cache-dir -r requirements.txt
>
> COPY ./app ./app
>
> COPY ./alembic.ini .
>
> COPY ./migrations ./migrations
>
> EXPOSE 8000
>
> CMD \[\"uvicorn\", \"app.main:app\", \"\--host\", \"0.0.0.0\", \"\--port\", \"8000\"\]

## **5.3 docker-compose.yml** {#docker-compose.yml}

> services:
>
> db:
>
> image: postgres:16-alpine
>
> environment:
>
> POSTGRES_USER: \${POSTGRES_USER}
>
> POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
>
> POSTGRES_DB: \${POSTGRES_DB}
>
> volumes:
>
> \- pgdata:/var/lib/postgresql/data
>
> healthcheck:
>
> test: \[\"CMD-SHELL\", \"pg_isready -U \${POSTGRES_USER}\"\]
>
> interval: 5s
>
> retries: 10
>
> networks: \[agecare-net\]
>
> migrations:
>
> build: .
>
> command: alembic upgrade head
>
> env_file: .env
>
> depends_on:
>
> db:
>
> condition: service_healthy
>
> networks: \[agecare-net\]
>
> api:
>
> build: .
>
> env_file: .env
>
> ports:
>
> \- \"8000:8000\"
>
> depends_on:
>
> migrations:
>
> condition: service_completed_successfully
>
> restart: unless-stopped
>
> networks: \[agecare-net\]
>
> worker:
>
> build: .
>
> command: python -m app.worker
>
> env_file: .env
>
> depends_on:
>
> migrations:
>
> condition: service_completed_successfully
>
> restart: unless-stopped
>
> networks: \[agecare-net\]
>
> volumes:
>
> pgdata:
>
> networks:
>
> agecare-net:

## **5.4 Variables de entorno** {#variables-de-entorno}

Ninguna credencial queda escrita en el código. Todas se definen en un archivo .env que no se versiona; el repositorio incluye un archivo .env.example con los nombres y valores de referencia.

| **Variable** | **Descripción** |
|:---|----|
| POSTGRES_USER | Usuario de la base de datos. |
| POSTGRES_PASSWORD | Contraseña de la base de datos. |
| POSTGRES_DB | Nombre de la base de datos. |
| DATABASE_URL | Cadena de conexión completa que utiliza la API. |
| JWT_SECRET | Clave para firmar los tokens de sesión. |
| ACCESS_TOKEN_MINUTES | Duración de la sesión en minutos. Valor por defecto: 30. |
| REFRESH_TOKEN_DAYS | Duración del token de renovación en días. Valor por defecto: 30. |
| STORAGE_URL | Dirección del servicio de almacenamiento de archivos. |
| PUSH_API_KEY | Credencial del servicio de notificaciones. |
| LLM_API_KEY | Credencial del modelo de lenguaje. |
| SPIKE_APP_ID | Identificador de la integración de wearables. |

## **5.5 Cómo levantar el sistema** {#cómo-levantar-el-sistema}

Los pasos quedan documentados en el archivo README.md del repositorio:

> git clone \<url-del-repositorio\>
>
> cd agecare-backend
>
> cp .env.example .env \# completar los valores
>
> docker compose up \--build \# levanta base de datos, migraciones, API y worker
>
> \# La API queda disponible en http://localhost:8000
>
> \# La documentación de los servicios en http://localhost:8000/docs

El contenedor de migraciones se ejecuta antes que la API y espera a que la base de datos responda, de modo que el sistema nunca arranca contra una estructura desactualizada. Para detenerlo se usa docker compose down; agregando la opción -v se elimina también el volumen con los datos.
