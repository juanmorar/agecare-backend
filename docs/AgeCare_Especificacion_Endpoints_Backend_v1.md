__AgeCare — Suite de Cuidado de Adultos Mayores__

__Especificación de Endpoints del Backend \(API REST\)__

Versión 1 · FastAPI \+ PostgreSQL en Azure

Rol: Especialista Backend

Fecha: 15 de julio de 2026

*Basado en: Documento de Funcionalidades v1 y Wireframes Familiar/Suite v1*

# __Contenido__

# __1\. Introducción y arquitectura de referencia__

Este documento especifica los endpoints del backend necesarios para implementar la versión 1 de la suite AgeCare, según el documento de funcionalidades y los wireframes de las vistas Familiar, Cuidadora y Adulto mayor\. Para cada endpoint se define su ruta, funcionalidad, roles autorizados, parámetros de entrada y salida con sus tipos, y los errores específicos con sus mensajes en español\.

## __1\.1 Stack tecnológico__

- API: FastAPI \(Python 3\.12\) con Pydantic v2 para validación de esquemas de entrada/salida, desplegada en Azure \(App Service o Container Apps\)\.
- Base de datos: Azure Database for PostgreSQL \(Flexible Server\), acceso vía SQLAlchemy 2 async \+ asyncpg; migraciones con Alembic\.
- Archivos: Azure Blob Storage con URLs firmadas \(SAS\) para subida y descarga directa desde la app\.
- Push: Azure Notification Hubs \(o FCM/APNs directo\) para el pilar de alertas\.
- IA: LLM para el asistente sobre el expediente; Azure AI Speech para TTS/STT; Azure AI Document Intelligence para OCR de recetas\.
- Tiempo real: WebSocket nativo de FastAPI para el chat; respaldo push cuando el cliente está desconectado\.
- Tareas programadas: worker \(Celery/APScheduler \+ Azure Service Bus o cron\) para generar dosis diarias, evaluar ventanas de medicación vencidas, detectar wearable sin datos y enviar recordatorios\.

## __1\.2 Módulos de la API__

La API se organiza en doce módulos \(routers de FastAPI\), correspondientes a las secciones 3 a 14 de este documento: autenticación, pacientes y onboarding, vitals y semáforo, medicamentos y adherencia, bitácora del expediente, archivos, alertas, asistente IA, mensajes, vista del adulto mayor, vista de la cuidadora y marketplace\.

# __2\. Convenciones generales de la API__

## __2\.1 URL base y versionado__

Todas las rutas REST cuelgan de https://api\.agecare\.app/api/v1\. El WebSocket del chat usa el prefijo /ws\. Los nombres de rutas y campos están en inglés \(convención de la industria\); las descripciones y los mensajes de error al usuario están en español\.

## __2\.2 Autenticación__

Salvo los endpoints públicos de la sección 3, toda petición requiere el encabezado Authorization: Bearer <access\_token>\. El access token es un JWT firmado \(HS256/RS256\) con vigencia de 30 minutos que incluye user\_id y roles por paciente; el refresh token dura 30 días y es rotatorio\. La autorización por recurso se valida contra la membresía del usuario en el paciente \(tabla patient\_members\)\.

## __2\.3 Paginación, orden y fechas__

Los listados usan paginación por página \(page, page\_size; máximo 100\) o por cursor cuando se indica \(chat\)\. Todas las fechas\-hora se transmiten en ISO 8601 UTC \(sufijo Z\); las fechas simples como date \(YYYY\-MM\-DD\)\. Los horarios de medicación se interpretan en la zona horaria del paciente \(campo timezone del perfil\)\.

## __2\.4 Formato estándar de error__

Todos los errores devuelven el mismo cuerpo JSON, apto para mostrarse directamente en la app:

__Campo__

__Tipo__

__Descripción__

error\.code

str

Código interno estable en MAYÚSCULAS \(ej\. PREMIUM\_REQUIRED\)\.

error\.message

str

Mensaje en español listo para mostrar al usuario\.

error\.details

list | null

Detalle por campo en errores de validación \(origen Pydantic\)\.

error\.request\_id

str

Identificador de la petición para soporte y trazabilidad\.

## __2\.5 Errores comunes a todos los endpoints__

Los siguientes errores aplican a cualquier endpoint autenticado y no se repiten en cada tabla:

__HTTP__

__Código interno__

__Mensaje__

401

UNAUTHORIZED

Tu sesión expiró\. Vuelve a iniciar sesión\.

403

FORBIDDEN

No tienes permisos para realizar esta acción sobre este paciente\.

404

NOT\_FOUND

El recurso solicitado no existe o no está disponible\.

422

VALIDATION\_ERROR

Hay datos inválidos en la solicitud\. Revisa los campos marcados\.

429

RATE\_LIMITED

Demasiadas solicitudes\. Intenta de nuevo en unos segundos\.

500

INTERNAL\_ERROR

Algo salió mal de nuestro lado\. Intenta más tarde\.

## __2\.6 Enumeraciones globales__

__Enum__

__Valores__

__Uso__

RoleType

family | caregiver | doctor | elder

Rol de un usuario respecto a un paciente\.

VitalType

heart\_rate | spo2 | sleep | steps | sedentary\_min | fall\_event | blood\_pressure | temperature | glucose

Tipos de vital \(wearable y manuales\)\.

WellbeingStatus

ok | warning | attention

Semáforo de bienestar\.

AlertType

fall | vital\_out\_of\_range | missed\_dose | sos | wearable\_offline

Tipos de alerta v1\.

AlertSeverity

info | warning | critical

Severidad de la alerta\.

DoseStatus

pending | taken | postponed | missed

Estado de una dosis programada\.

PlanType

free | premium

Plan de la cuidadora\.

## __2\.7 Matriz de permisos por rol__

Resumen del principio de separación de roles: el familiar observa, la cuidadora opera, el médico prescribe y el adulto mayor se comunica\. Leyenda: L = lectura, E = escritura, — = sin acceso\.

__Recurso__

__Familiar__

__Cuidadora__

__Médico__

__Adulto mayor__

Perfil del paciente

E \(owner\)

L

L

L

Invitaciones y miembros

E \(owner\)

—

L

—

Vitals \(wearable y series\)

L

L \+ E \(manuales\)

L

L \(propio\)

Umbrales de alerta

E

L

E

—

Plan de medicamentos

L

E

E

—

Registro de dosis \(adherencia\)

L

E

L

—

Observaciones e incidentes

L

E

L

E \(check\-in\)

Documentos médicos

E

E

E

—

Alertas \(ver / atender\)

L \+ E

L \+ E

L

—

Asistente IA

E

E

E

E

Chat del paciente

E

E

L

E

Galería de fotos

E \(publica\)

E \(Premium\)

—

L \+ reacciones

Entretenimiento \(feed\)

L

—

—

L

Tareas del día

L \+ E

E

—

—

SOS

recibe

E

—

E

Marketplace

L \+ contacto

E \(su perfil\)

—

—

# __3\. Autenticación y cuenta de usuario__

Autenticación propia con JWT emitidos por FastAPI \(access token de corta duración \+ refresh token rotatorio persistido en PostgreSQL\)\. Las contraseñas se almacenan con hash bcrypt/argon2\. Incluye el registro del dispositivo móvil para notificaciones push\.

### __3\.1 Registrar cuenta__

__ POST   /api/v1/auth/register__

Crea la cuenta del usuario\. En el flujo v1 el familiar es quien se registra directamente; cuidadora, médico y adulto mayor se registran a través de una invitación \(ver 4\.5\), pasando el campo invitation\_token\.

__Roles autorizados: __Público \(sin token\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

full\_name

str \(2–120\)

body

Sí

Nombre completo del usuario\.

email

EmailStr

body

Sí

Correo electrónico único; se usa como identificador de acceso\.

password

str \(min 8\)

body

Sí

Contraseña; mínimo 8 caracteres, al menos una letra y un número\.

phone

str | null

body

No

Teléfono de contacto en formato E\.164\.

invitation\_token

str | null

body

No

Token de invitación; si se envía, la cuenta se crea con el rol y paciente de la invitación\.

locale

str

body

No

Idioma preferido \(es, en\)\. Por defecto: es\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

user\_id

UUID

Identificador del usuario creado\.

email

EmailStr

Correo registrado\.

role

enum RoleType | null

Rol asignado si vino de invitación \(family | caregiver | doctor | elder\)\.

access\_token

str \(JWT\)

Token de acceso \(exp\. 30 min\)\.

refresh\_token

str

Token de refresco \(exp\. 30 días, rotatorio\)\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

EMAIL\_ALREADY\_EXISTS

Ya existe una cuenta con este correo electrónico\.

400

WEAK\_PASSWORD

La contraseña no cumple los requisitos mínimos de seguridad\.

400

INVALID\_INVITATION

La invitación no existe, ya fue usada o está vencida\.

### __3\.2 Iniciar sesión__

__ POST   /api/v1/auth/login__

Autentica con correo y contraseña y devuelve el par de tokens\. La respuesta incluye los roles del usuario por paciente para que la app muestre la vista correcta \(familiar, cuidadora, médico o adulto mayor\)\.

__Roles autorizados: __Público \(sin token\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

email

EmailStr

body

Sí

Correo de la cuenta\.

password

str

body

Sí

Contraseña\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

access\_token

str \(JWT\)

Token de acceso\.

refresh\_token

str

Token de refresco\.

user

UserOut

Perfil básico: user\_id, full\_name, email, locale\.

memberships

list\[MembershipOut\]

Lista de \{patient\_id: UUID, patient\_name: str, role: enum RoleType\}\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

401

INVALID\_CREDENTIALS

Correo o contraseña incorrectos\.

423

ACCOUNT\_LOCKED

Cuenta bloqueada temporalmente por intentos fallidos\. Intenta en 15 minutos\.

### __3\.3 Refrescar token__

__ POST   /api/v1/auth/refresh__

Intercambia un refresh token válido por un nuevo par de tokens\. El refresh token usado se invalida \(rotación\) para mitigar robo de tokens\.

__Roles autorizados: __Público \(requiere refresh token válido\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

refresh\_token

str

body

Sí

Refresh token vigente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

access\_token

str \(JWT\)

Nuevo token de acceso\.

refresh\_token

str

Nuevo token de refresco\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

401

INVALID\_REFRESH\_TOKEN

El token de refresco es inválido, expiró o ya fue utilizado\.

### __3\.4 Cerrar sesión__

__ POST   /api/v1/auth/logout__

Revoca el refresh token activo y desasocia el dispositivo push si se indica\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

refresh\_token

str

body

Sí

Refresh token a revocar\.

device\_id

UUID | null

body

No

Dispositivo push a desactivar\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

### __3\.5 Solicitar recuperación de contraseña__

__ POST   /api/v1/auth/password/recovery__

Envía un correo con un código/enlace de restablecimiento\. Siempre responde 202 aunque el correo no exista \(evita enumeración de cuentas\)\.

__Roles autorizados: __Público \(sin token\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

email

EmailStr

body

Sí

Correo de la cuenta\.

__Respuesta exitosa: 202 Accepted \(sin cuerpo\)\.__

### __3\.6 Restablecer contraseña__

__ POST   /api/v1/auth/password/reset__

Establece una nueva contraseña usando el token recibido por correo\. Revoca todas las sesiones activas\.

__Roles autorizados: __Público \(sin token\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

reset\_token

str

body

Sí

Token del correo de recuperación \(exp\. 30 min\)\.

new\_password

str \(min 8\)

body

Sí

Nueva contraseña\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

INVALID\_RESET\_TOKEN

El enlace de recuperación es inválido o expiró\. Solicita uno nuevo\.

400

WEAK\_PASSWORD

La contraseña no cumple los requisitos mínimos de seguridad\.

### __3\.7 Obtener mi perfil__

__ GET   /api/v1/users/me__

Devuelve el perfil del usuario autenticado y sus membresías \(pacientes y rol en cada uno\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

user\_id

UUID

Identificador\.

full\_name

str

Nombre completo\.

email

EmailStr

Correo\.

phone

str | null

Teléfono\.

avatar\_url

HttpUrl | null

Foto de perfil\.

locale

str

Idioma\.

memberships

list\[MembershipOut\]

Pacientes y rol en cada uno\.

### __3\.8 Actualizar mi perfil__

__ PATCH   /api/v1/users/me__

Actualización parcial del perfil propio \(nombre, teléfono, avatar, idioma\)\. El correo no se cambia por esta vía\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

full\_name

str | null

body

No

Nuevo nombre\.

phone

str | null

body

No

Nuevo teléfono\.

avatar\_url

HttpUrl | null

body

No

URL del avatar \(subido vía 8\.1\)\.

locale

str | null

body

No

Idioma preferido\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(perfil\)

UserOut

Perfil actualizado, mismo esquema que GET /users/me\.

### __3\.9 Registrar dispositivo push__

__ POST   /api/v1/users/me/devices__

Registra \(o actualiza, si ya existe el token\) el dispositivo móvil para notificaciones push vía FCM/APNs\. Necesario para el pilar de alertas\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

push\_token

str

body

Sí

Token FCM o APNs del dispositivo\.

platform

enum: ios | android

body

Sí

Plataforma del dispositivo\.

app\_version

str | null

body

No

Versión de la app instalada\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

device\_id

UUID

Identificador del registro de dispositivo\.

# __4\. Pacientes, roles y onboarding__

El familiar crea el perfil del paciente e invita al resto del círculo de cuidado \(cuidadora, médico, adulto mayor y otros familiares\)\. Todos los recursos clínicos cuelgan de patient\_id y el acceso se valida contra la tabla de membresías \(patient\_members\)\.

### __4\.1 Crear paciente__

__ POST   /api/v1/patients__

Crea el perfil del adulto mayor\. Quien lo crea queda registrado automáticamente como familiar administrador \(owner\) del paciente\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

full\_name

str \(2–120\)

body

Sí

Nombre del adulto mayor\.

birth\_date

date

body

Sí

Fecha de nacimiento \(ISO 8601\)\.

sex

enum: female | male | other

body

No

Sexo\.

photo\_url

HttpUrl | null

body

No

Foto de perfil\.

conditions

list\[str\]

body

No

Padecimientos relevantes \(texto libre corto\)\.

notes

str | null

body

No

Notas generales del expediente\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

patient\_id

UUID

Identificador del paciente\.

full\_name

str

Nombre\.

created\_at

datetime

Fecha de creación\.

### __4\.2 Listar mis pacientes__

__ GET   /api/v1/patients__

Lista los pacientes a los que el usuario tiene acceso \(soporte multi\-paciente\)\. Alimenta el selector de paciente persistente de la app\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[PatientCardOut\]

Lista de \{patient\_id, full\_name, photo\_url, role, wellbeing\_status: enum ok | warning | attention\}\.

### __4\.3 Detalle de paciente__

__ GET   /api/v1/patients/\{patient\_id\}__

Devuelve el perfil completo del paciente, incluyendo el estado del wearable vinculado\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Identificador del paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

patient\_id

UUID

Identificador\.

full\_name

str

Nombre\.

birth\_date

date

Fecha de nacimiento\.

sex

enum | null

Sexo\.

photo\_url

HttpUrl | null

Foto\.

conditions

list\[str\]

Padecimientos\.

notes

str | null

Notas\.

wearable

WearableOut | null

Wearable vinculado: \{wearable\_id, model, last\_sync\_at: datetime, battery\_pct: int\}\.

### __4\.4 Actualizar paciente__

__ PATCH   /api/v1/patients/\{patient\_id\}__

Actualización parcial del perfil del paciente\. Solo el familiar administrador puede editarlo\.

__Roles autorizados: __Familiar \(owner\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Identificador del paciente\.

full\_name / birth\_date / sex / photo\_url / conditions / notes

\(los del POST\)

body

No

Cualquier subconjunto de los campos de creación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(paciente\)

PatientOut

Perfil actualizado\.

### __4\.5 Invitar miembro al círculo de cuidado__

__ POST   /api/v1/patients/\{patient\_id\}/invitations__

Genera una invitación con token de un solo uso \(enviada por correo o compartible como enlace\) para incorporar a una cuidadora, médico, otro familiar o al adulto mayor\.

__Roles autorizados: __Familiar \(owner\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente al que se invita\.

role

enum RoleType

body

Sí

Rol a otorgar: family | caregiver | doctor | elder\.

email

EmailStr | null

body

No

Correo del invitado; si se omite, se devuelve solo el enlace para compartir\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

invitation\_id

UUID

Identificador\.

token

str

Token de un solo uso \(exp\. 7 días\)\.

invite\_url

HttpUrl

Enlace profundo para aceptar la invitación\.

expires\_at

datetime

Vencimiento\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

MEMBER\_ALREADY\_EXISTS

Esta persona ya forma parte del círculo de cuidado del paciente\.

409

ELDER\_ALREADY\_LINKED

El paciente ya tiene una cuenta de adulto mayor vinculada\.

### __4\.6 Aceptar invitación__

__ POST   /api/v1/invitations/accept__

Acepta una invitación con el token\. Si quien la acepta ya tiene cuenta, se agrega la membresía; si no, primero debe registrarse \(3\.1\) pasando invitation\_token\.

__Roles autorizados: __Cualquier usuario autenticado

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

token

str

body

Sí

Token de la invitación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

patient\_id

UUID

Paciente al que se unió\.

role

enum RoleType

Rol otorgado\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

INVALID\_INVITATION

La invitación no existe, ya fue usada o está vencida\.

### __4\.7 Listar círculo de cuidado__

__ GET   /api/v1/patients/\{patient\_id\}/members__

Lista los miembros vinculados al paciente con su rol, además de las invitaciones pendientes\. Alimenta la pantalla “Roles e invitaciones”\.

__Roles autorizados: __Familiar, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Identificador del paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

members

list\[MemberOut\]

\{user\_id, full\_name, email, role, joined\_at: datetime\}\.

pending\_invitations

list\[InvitationOut\]

\{invitation\_id, email, role, expires\_at\}\.

### __4\.8 Quitar miembro__

__ DELETE   /api/v1/patients/\{patient\_id\}/members/\{user\_id\}__

Revoca el acceso de un miembro al paciente\. No puede eliminarse al propio owner\.

__Roles autorizados: __Familiar \(owner\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

user\_id

UUID

path

Sí

Miembro a quitar\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

CANNOT\_REMOVE\_OWNER

No puedes quitar al administrador del paciente\.

### __4\.9 Vincular wearable__

__ POST   /api/v1/patients/\{patient\_id\}/wearable__

Asocia un dispositivo wearable al paciente durante el onboarding\. Un paciente tiene como máximo un wearable activo; volver a llamar reemplaza el anterior\.

__Roles autorizados: __Familiar, Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

serial\_number

str

body

Sí

Número de serie del dispositivo\.

model

str

body

Sí

Modelo del wearable\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

wearable\_id

UUID

Identificador del vínculo\.

linked\_at

datetime

Fecha de vinculación\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

WEARABLE\_IN\_USE

Este dispositivo ya está vinculado a otro paciente\.

### __4\.10 Estado de sincronización del wearable__

__ GET   /api/v1/patients/\{patient\_id\}/wearable/status__

Devuelve el estado de sincronización para detectar lagunas de datos: última lectura recibida, batería reportada y bandera de desconexión \(sin datos por más de la ventana configurada\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

wearable\_id

UUID | null

Wearable activo; null si no hay\.

last\_sync\_at

datetime | null

Última lectura recibida\.

battery\_pct

int \(0–100\) | null

Última batería reportada\.

is\_stale

bool

true si no hay datos en más de 2 horas\.

# __5\. Vitals y resumen del día \(semáforo\)__

Lecturas del wearable ingeridas en lote desde la app móvil, vitals manuales capturados por la cuidadora, umbrales configurables por vital y el semáforo de bienestar que resume el día\. Las lecturas se almacenan en una tabla particionada por mes \(vital\_readings\) para consultas de tendencia eficientes\.

### __5\.1 Ingesta de lecturas del wearable \(lote\)__

__ POST   /api/v1/patients/\{patient\_id\}/vitals/batch__

Recibe un lote de lecturas sincronizadas por la app móvil desde el wearable\. La operación es idempotente: lecturas duplicadas \(misma fuente, tipo y timestamp\) se descartan silenciosamente\. Tras insertar, el motor de alertas evalúa umbrales y caídas\.

__Roles autorizados: __Cuidadora, Adulto mayor \(dispositivo\), Familiar

*Las caídas detectadas por el wearable se envían aquí como lecturas type=fall\_event y disparan la alerta crítica en tiempo real \(sección 9\)\.*

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

readings

list\[VitalReadingIn\] \(1–500\)

body

Sí

Lecturas del lote\.

readings\[\]\.type

enum VitalType

body

Sí

heart\_rate | spo2 | sleep | steps | sedentary\_min | fall\_event\.

readings\[\]\.value

float

body

Sí

Valor numérico \(bpm, %, horas, pasos, min; 1 para fall\_event\)\.

readings\[\]\.measured\_at

datetime \(UTC\)

body

Sí

Momento de la medición\.

readings\[\]\.meta

dict | null

body

No

Datos extra del fabricante \(JSON\)\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

accepted

int

Lecturas insertadas\.

duplicates

int

Lecturas descartadas por duplicado\.

alerts\_triggered

int

Alertas generadas por este lote\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

BATCH\_TOO\_LARGE

El lote excede el máximo de 500 lecturas\.

### __5\.2 Registrar vital manual__

__ POST   /api/v1/patients/\{patient\_id\}/vitals/manual__

La cuidadora registra un vital medido manualmente \(presión arterial, temperatura, glucosa\) como complemento al wearable o cuando no lo hay\. También se evalúa contra umbrales\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

type

enum: blood\_pressure | temperature | glucose | heart\_rate | spo2

body

Sí

Tipo de vital manual\.

value

float

body

Sí

Valor principal \(sistólica si es presión\)\.

value\_secondary

float | null

body

No

Valor secundario \(diastólica si es presión\)\.

measured\_at

datetime | null

body

No

Momento de la medición; por defecto, ahora\.

note

str | null

body

No

Comentario breve\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

reading\_id

UUID

Identificador de la lectura\.

alert\_triggered

bool

Si generó alerta por umbral\.

### __5\.3 Consultar vitals \(series y tendencias\)__

__ GET   /api/v1/patients/\{patient\_id\}/vitals__

Devuelve la serie temporal de un vital con agregación por hora, día o semana para las mini\-gráficas de tendencia \(semanal/mensual\) de la pantalla de Salud\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

type

enum VitalType

query

Sí

Vital a consultar\.

date\_from

date

query

Sí

Inicio del rango\.

date\_to

date

query

Sí

Fin del rango \(máx\. 92 días\)\.

granularity

enum: raw | hour | day | week

query

No

Agregación; por defecto day\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

type

enum VitalType

Vital consultado\.

unit

str

Unidad \(bpm, %, h, pasos, min\)\.

points

list\[VitalPointOut\]

\{ts: datetime, value: float, min: float | null, max: float | null\}\.

threshold

ThresholdOut | null

Umbral vigente para dibujar la línea de referencia\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

RANGE\_TOO\_WIDE

El rango solicitado excede el máximo de 92 días\.

### __5\.4 Últimos valores de vitals__

__ GET   /api/v1/patients/\{patient\_id\}/vitals/latest__

Devuelve el valor más reciente de cada vital para las tarjetas resumen de Inicio/Hoy\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[LatestVitalOut\]

\{type, value, unit, measured\_at, in\_range: bool\}\.

### __5\.5 Consultar umbrales de alerta__

__ GET   /api/v1/patients/\{patient\_id\}/vitals/thresholds__

Lista los umbrales configurados por vital \(ej\. SpO2 mínimo, rango de ritmo cardíaco\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ThresholdOut\]

\{type, min\_value: float | null, max\_value: float | null, updated\_by: UUID, updated\_at\}\.

### __5\.6 Configurar umbral de un vital__

__ PUT   /api/v1/patients/\{patient\_id\}/vitals/thresholds/\{type\}__

Crea o reemplaza el umbral de un vital\. Al menos uno de min\_value o max\_value debe enviarse\.

__Roles autorizados: __Familiar, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

type

enum VitalType

path

Sí

Vital a configurar\.

min\_value

float | null

body

No\*

Valor mínimo permitido\.

max\_value

float | null

body

No\*

Valor máximo permitido\. \(\*al menos uno de los dos\)

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(umbral\)

ThresholdOut

Umbral resultante\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

EMPTY\_THRESHOLD

Debes indicar al menos un valor mínimo o máximo\.

400

INVALID\_THRESHOLD\_RANGE

El mínimo no puede ser mayor que el máximo\.

### __5\.7 Resumen del día \(semáforo\)__

__ GET   /api/v1/patients/\{patient\_id\}/summary/today__

Calcula y devuelve el semáforo de bienestar del día del paciente a partir de vitals en rango, adherencia a medicamentos y eventos \(caídas, SOS\), junto con las tarjetas resumen de Inicio/Hoy\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

wellbeing\_status

enum: ok | warning | attention

Semáforo del día \(bien / regular / requiere atención\)\.

status\_reasons

list\[str\]

Motivos legibles \(ej\. “SpO2 bajo a las 10:32”\)\.

active\_alerts

list\[AlertOut\]

Alertas activas para la banda superior\.

latest\_vitals

list\[LatestVitalOut\]

Vitals clave más recientes\.

medications\_today

MedsTodayOut

\{taken: int, pending: int, missed: int, next\_dose: DoseOut | null\}\.

last\_observation

ObservationOut | null

Última observación de la cuidadora\.

### __5\.8 Tablero multi\-paciente__

__ GET   /api/v1/users/me/dashboard__

Devuelve una tarjeta\-semáforo por cada paciente del usuario, para el Inicio cuando hay más de un paciente\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[PatientCardOut\]

\{patient\_id, full\_name, photo\_url, wellbeing\_status, active\_alerts\_count: int, top\_reason: str | null\}\.

# __6\. Medicamentos y adherencia__

Plan de medicamentos configurado por cuidadora o médico \(o importado por OCR de receta\), generación diaria de dosis programadas, registro de administración y métricas de adherencia\. El familiar visualiza pero no edita \(separación observar vs\. operar\)\. Una dosis no confirmada dentro de su ventana genera alerta automática \(sección 9\)\.

### __6\.1 Crear medicamento del plan__

__ POST   /api/v1/patients/\{patient\_id\}/medications__

Agrega un medicamento al plan con su dosis y horarios\. El backend genera las dosis programadas diarias \(scheduled\_doses\) a partir de los horarios\.

__Roles autorizados: __Cuidadora, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

name

str \(2–120\)

body

Sí

Nombre del medicamento\.

dose

str

body

Sí

Dosis y unidad \(ej\. “50 mg”, “10 gotas”\)\.

instructions

str | null

body

No

Indicaciones \(ej\. “con alimentos”\)\.

times

list\[time\] \(1–8\)

body

Sí

Horarios de toma \(hora local del paciente\)\.

days\_of\_week

list\[int 0–6\] | null

body

No

Días de la semana; por defecto todos\.

start\_date

date

body

Sí

Inicio del tratamiento\.

end\_date

date | null

body

No

Fin del tratamiento; null = indefinido\.

grace\_window\_min

int \(5–240\)

body

No

Ventana en minutos antes de marcar la dosis como no tomada\. Por defecto 60\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

medication\_id

UUID

Identificador\.

name

str

Nombre\.

prescribed\_by

UUID | null

Médico que lo prescribió, si aplica\.

created\_at

datetime

Fecha de alta\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

INVALID\_DATE\_RANGE

La fecha de fin no puede ser anterior a la de inicio\.

### __6\.2 Listar plan de medicamentos__

__ GET   /api/v1/patients/\{patient\_id\}/medications__

Lista los medicamentos del plan, activos e históricos\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

active\_only

bool

query

No

Solo vigentes\. Por defecto true\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[MedicationOut\]

\{medication\_id, name, dose, instructions, times, days\_of\_week, start\_date, end\_date, prescribed\_by, is\_active: bool\}\.

### __6\.3 Actualizar medicamento__

__ PATCH   /api/v1/patients/\{patient\_id\}/medications/\{medication\_id\}__

Modifica dosis, horarios o vigencia\. Las dosis futuras se regeneran; las pasadas no se alteran\.

__Roles autorizados: __Cuidadora, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

medication\_id

UUID

path

Sí

Medicamento\.

\(campos del POST\)

—

body

No

Cualquier subconjunto de los campos de creación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(medicamento\)

MedicationOut

Medicamento actualizado\.

### __6\.4 Descontinuar medicamento__

__ DELETE   /api/v1/patients/\{patient\_id\}/medications/\{medication\_id\}__

Baja lógica: marca el medicamento como descontinuado y cancela sus dosis futuras\. El historial de adherencia se conserva\.

__Roles autorizados: __Cuidadora, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

medication\_id

UUID

path

Sí

Medicamento\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

### __6\.5 Dosis del día / agenda de tomas__

__ GET   /api/v1/patients/\{patient\_id\}/doses__

Devuelve las dosis programadas de una fecha con su estado, para el check\-in de la cuidadora y la tarjeta de medicamentos del familiar\. Incluye la próxima toma con cuenta regresiva\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

date

date

query

No

Fecha consultada; por defecto hoy\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[DoseOut\]

\{dose\_id, medication\_id, medication\_name, dose, scheduled\_at: datetime, status: enum pending | taken | postponed | missed, logged\_by: UUID | null, logged\_at: datetime | null, reason: str | null\}\.

next\_dose

DoseOut | null

Próxima dosis pendiente del día\.

### __6\.6 Registrar administración de dosis__

__ POST   /api/v1/doses/\{dose\_id\}/log__

La cuidadora confirma una dosis como administrada, pospuesta u omitida \(con motivo\)\. Detiene el recordatorio persistente\. Si el estado es omitida, se notifica al familiar\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

dose\_id

UUID

path

Sí

Dosis programada\.

status

enum: taken | postponed | missed

body

Sí

Resultado de la toma\.

postponed\_until

datetime | null

body

No

Obligatorio si status=postponed; máx\. \+4 h\.

reason

str | null

body

No

Motivo \(obligatorio si status=missed\)\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

dose\_id

UUID

Dosis actualizada\.

status

enum

Estado registrado\.

alert\_triggered

bool

Si se alertó al familiar\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

DOSE\_ALREADY\_LOGGED

Esta dosis ya fue registrada\.

400

MISSING\_REASON

Debes indicar el motivo cuando la dosis se marca como omitida\.

400

INVALID\_POSTPONE\_TIME

La dosis solo puede posponerse hasta 4 horas\.

### __6\.7 Métricas de adherencia__

__ GET   /api/v1/patients/\{patient\_id\}/adherence__

Resumen de adherencia en un rango: porcentaje global, desglose por medicamento y serie diaria para gráficas\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

date\_from

date

query

Sí

Inicio del rango\.

date\_to

date

query

Sí

Fin del rango\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

adherence\_pct

float \(0–100\)

Porcentaje de dosis tomadas a tiempo\.

taken

int

Dosis tomadas\.

missed

int

Dosis omitidas\.

by\_medication

list\[MedAdherenceOut\]

\{medication\_id, name, adherence\_pct\}\.

daily

list\[DailyAdherenceOut\]

\{date, taken, missed, pending\}\.

### __6\.8 Digitalizar receta \(OCR\)__

__ POST   /api/v1/patients/\{patient\_id\}/prescriptions/scan__

Recibe la foto de una receta, ejecuta OCR \(Azure AI Document Intelligence\) y devuelve una propuesta de plan de medicamentos que la cuidadora/médico revisa y confirma creando los medicamentos \(6\.1\)\. La imagen queda guardada como documento del expediente\.

__Roles autorizados: __Cuidadora, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

file

binary \(multipart, jpg/png/pdf, máx\. 10 MB\)

body

Sí

Imagen o PDF de la receta\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

document\_id

UUID

Documento creado en el repositorio\.

suggestions

list\[MedSuggestionOut\]

\{name, dose, times, confidence: float 0–1\} por medicamento detectado\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

UNSUPPORTED\_FILE\_TYPE

Formato no soportado\. Usa JPG, PNG o PDF\.

413

FILE\_TOO\_LARGE

El archivo excede el máximo de 10 MB\.

422

OCR\_FAILED

No pudimos leer la receta\. Intenta con una foto más nítida\.

# __7\. Observaciones, incidentes, check\-in y documentos__

La bitácora del expediente: observaciones de la cuidadora \(con foto opcional\), incidentes con hora y detalle, notas de relevo entre turnos, el check\-in emocional del adulto mayor y el repositorio de documentos médicos en Azure Blob Storage\. Todo este contenido es consultable por el asistente IA\.

### __7\.1 Registrar observación__

__ POST   /api/v1/patients/\{patient\_id\}/observations__

La cuidadora registra una observación del día \(ánimo, apetito, sueño, incidencia, nota general\) con foto opcional\. El check\-in del adulto mayor \(7\.4\) también crea entradas aquí\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

category

enum: mood | appetite | sleep | hygiene | activity | incident\_note | general

body

Sí

Categoría de la observación\.

text

str \(1–2000\)

body

Sí

Contenido de la observación\.

photo\_upload\_id

UUID | null

body

No

Foto adjunta previamente subida \(8\.1\)\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

observation\_id

UUID

Identificador\.

created\_at

datetime

Fecha de registro\.

### __7\.2 Consultar bitácora de observaciones__

__ GET   /api/v1/patients/\{patient\_id\}/observations__

Lista paginada de observaciones, con filtros por categoría, autor y rango de fechas\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

category

enum | null

query

No

Filtro por categoría\.

date\_from / date\_to

date

query

No

Rango de fechas\.

page / page\_size

int

query

No

Paginación \(por defecto 1 / 20, máx\. 100\)\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ObservationOut\]

\{observation\_id, category, text, photo\_url, author: \{user\_id, full\_name, role\}, created\_at\}\.

total / page / page\_size

int

Metadatos de paginación\.

### __7\.3 Registrar incidente__

__ POST   /api/v1/patients/\{patient\_id\}/incidents__

Registra un incidente presenciado \(ej\. una caída\) con hora y detalle\. Si severity=critical se genera además una alerta al familiar\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

type

enum: fall | pain | confusion | wandering | other

body

Sí

Tipo de incidente\.

severity

enum: low | medium | critical

body

Sí

Gravedad\.

occurred\_at

datetime

body

Sí

Hora del incidente\.

description

str \(1–2000\)

body

Sí

Detalle de lo ocurrido\.

photo\_upload\_id

UUID | null

body

No

Foto adjunta\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

incident\_id

UUID

Identificador\.

alert\_triggered

bool

Si generó alerta\.

### __7\.4 Nota de relevo entre turnos__

__ POST   /api/v1/patients/\{patient\_id\}/handover\-notes__

La cuidadora deja el contexto del turno para la siguiente cuidadora \(pendientes, estado general, indicaciones\)\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

text

str \(1–2000\)

body

Sí

Contenido de la nota de relevo\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

note\_id

UUID

Identificador\.

created\_at

datetime

Fecha\.

### __7\.5 Consultar notas de relevo__

__ GET   /api/v1/patients/\{patient\_id\}/handover\-notes__

Lista las notas de relevo más recientes \(por defecto las de las últimas 72 horas\)\.

__Roles autorizados: __Cuidadora, Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

limit

int

query

No

Máximo de notas; por defecto 10\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[HandoverNoteOut\]

\{note\_id, text, author, created\_at\}\.

### __7\.6 Check\-in del adulto mayor__

__ POST   /api/v1/patients/\{patient\_id\}/checkin__

El adulto mayor responde “¿Cómo me siento hoy?” con caritas \(bien / regular / mal\)\. La respuesta alimenta la bitácora de observaciones y el semáforo del día\. Máximo un check\-in por día; uno nuevo reemplaza al anterior\.

__Roles autorizados: __Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente \(su propio perfil\)\.

feeling

enum: good | regular | bad

body

Sí

Cómo se siente hoy\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

checkin\_id

UUID

Identificador\.

date

date

Día del check\-in\.

# __8\. Archivos y documentos médicos__

Subida de archivos en dos pasos con URLs firmadas \(SAS\) de Azure Blob Storage: primero se solicita la URL de subida, la app sube el binario directo a Blob, y después se confirma/asocia el archivo\. Las descargas también usan URLs firmadas de corta duración\. Aplica a documentos médicos, fotos de observaciones, fotos de la galería familiar y notas de voz\.

### __8\.1 Solicitar URL de subida \(genérico\)__

__ POST   /api/v1/uploads__

Genera una URL SAS de escritura para subir un archivo directamente a Azure Blob\. Devuelve un upload\_id que luego se referencia al crear el recurso \(observación, foto, documento, mensaje de voz\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

purpose

enum: document | observation\_photo | gallery\_photo | voice\_note | avatar | chat\_media

body

Sí

Uso del archivo \(determina contenedor y validaciones\)\.

file\_name

str

body

Sí

Nombre original del archivo\.

content\_type

str \(MIME\)

body

Sí

Tipo MIME \(ej\. image/jpeg, audio/m4a, application/pdf\)\.

size\_bytes

int

body

Sí

Tamaño; máx\. 25 MB \(10 MB imágenes, 5 MB audio\)\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

upload\_id

UUID

Identificador para asociar el archivo\.

upload\_url

HttpUrl \(SAS\)

URL firmada para PUT del binario \(exp\. 15 min\)\.

expires\_at

datetime

Vencimiento de la URL\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

UNSUPPORTED\_FILE\_TYPE

Tipo de archivo no permitido para este uso\.

413

FILE\_TOO\_LARGE

El archivo excede el tamaño máximo permitido\.

### __8\.2 Registrar documento médico__

__ POST   /api/v1/patients/\{patient\_id\}/documents__

Asocia un archivo ya subido \(8\.1\) al repositorio de documentos del expediente \(recetas, estudios, indicaciones\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

upload\_id

UUID

body

Sí

Archivo subido\.

title

str \(1–150\)

body

Sí

Título del documento\.

category

enum: prescription | lab\_result | medical\_report | instruction | other

body

Sí

Categoría\.

doc\_date

date | null

body

No

Fecha del documento\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

document\_id

UUID

Identificador\.

created\_at

datetime

Fecha de registro\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

UPLOAD\_NOT\_FOUND

El archivo referenciado no existe o no se completó la subida\.

### __8\.3 Listar documentos__

__ GET   /api/v1/patients/\{patient\_id\}/documents__

Lista paginada del repositorio de documentos con filtro por categoría\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

category

enum | null

query

No

Filtro por categoría\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[DocumentOut\]

\{document\_id, title, category, doc\_date, content\_type, size\_bytes, uploaded\_by, created\_at\}\.

total

int

Total de documentos\.

### __8\.4 Descargar documento__

__ GET   /api/v1/documents/\{document\_id\}/download__

Devuelve una URL SAS de lectura de corta duración para ver o descargar el archivo\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

document\_id

UUID

path

Sí

Documento\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

download\_url

HttpUrl \(SAS\)

URL firmada de lectura \(exp\. 15 min\)\.

### __8\.5 Eliminar documento__

__ DELETE   /api/v1/documents/\{document\_id\}__

Elimina el documento del repositorio \(baja lógica; el blob se depura después por política de retención\)\.

__Roles autorizados: __Familiar \(owner\), quien lo subió

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

document\_id

UUID

path

Sí

Documento\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

# __9\. Alertas y notificaciones \(pilar central\)__

Las alertas se generan en el backend a partir de: \(a\) vitals fuera del umbral configurado, \(b\) eventos de caída del wearable o incidentes críticos, \(c\) dosis no confirmadas dentro de su ventana, y \(d\) botón SOS de la cuidadora\. Cada alerta dispara push \(FCM/APNs\) según las preferencias del usuario y queda en el centro de alertas \(campana\) con su historial\. Las caídas son críticas y abren el flujo de acción inmediata en la app\.

### __9\.1 Centro de alertas \(todas\)__

__ GET   /api/v1/users/me/alerts__

Lista las alertas de todos los pacientes del usuario, para la campana\. Filtro por estado y paciente; paginada, ordenada por fecha descendente\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

status

enum: active | acknowledged | resolved | all

query

No

Filtro por estado; por defecto active\.

patient\_id

UUID | null

query

No

Filtrar por paciente\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[AlertOut\]

\{alert\_id, patient\_id, patient\_name, type: enum fall | vital\_out\_of\_range | missed\_dose | sos | wearable\_offline, severity: enum info | warning | critical, title, detail, payload: dict, status, created\_at, acknowledged\_by: UUID | null, resolved\_at: datetime | null\}\.

total / unread\_count

int

Total y no leídas \(para el badge de la campana\)\.

### __9\.2 Marcar alerta como atendida__

__ POST   /api/v1/alerts/\{alert\_id\}/acknowledge__

El usuario indica que vio la alerta y se está haciendo cargo\. Detiene los recordatorios push de esa alerta\.

__Roles autorizados: __Familiar, Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

alert\_id

UUID

path

Sí

Alerta\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

alert\_id

UUID

Alerta\.

status

enum

Nuevo estado: acknowledged\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

ALERT\_ALREADY\_CLOSED

La alerta ya fue atendida o resuelta\.

### __9\.3 Resolver alerta__

__ POST   /api/v1/alerts/\{alert\_id\}/resolve__

Cierra la alerta con una nota de resolución \(ej\. “falsa alarma”, “se llamó a emergencias”\)\. Queda en el historial\.

__Roles autorizados: __Familiar, Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

alert\_id

UUID

path

Sí

Alerta\.

resolution\_note

str | null

body

No

Nota de cierre\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

alert\_id

UUID

Alerta\.

status

enum

Nuevo estado: resolved\.

### __9\.4 Consultar preferencias de notificación__

__ GET   /api/v1/users/me/notification\-settings__

Preferencias push por tipo de alerta\. Las alertas críticas \(caída, SOS\) no pueden desactivarse\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[NotifSettingOut\]

\{alert\_type, push\_enabled: bool, is\_locked: bool \(crítica, no desactivable\)\}\.

### __9\.5 Actualizar preferencias de notificación__

__ PUT   /api/v1/users/me/notification\-settings__

Activa/desactiva push por tipo de alerta no crítica\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

items

list\[NotifSettingIn\]

body

Sí

\{alert\_type: enum, push\_enabled: bool\}\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[NotifSettingOut\]

Preferencias resultantes\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

CRITICAL\_ALERT\_LOCKED

Las alertas de caída y SOS no pueden desactivarse\.

### __9\.6 Disparar SOS__

__ POST   /api/v1/patients/\{patient\_id\}/sos__

Botón de emergencia de la cuidadora \(siempre visible\)\. Crea una alerta crítica, notifica push inmediato a todos los familiares y registra el evento en el expediente con hora\. La respuesta incluye teléfonos de contacto para el flujo de llamada\.

__Roles autorizados: __Cuidadora, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

note

str | null

body

No

Descripción breve de la emergencia\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

alert\_id

UUID

Alerta crítica creada\.

notified\_count

int

Familiares notificados\.

emergency\_contacts

list\[ContactOut\]

\{full\_name, phone, role\} para llamar desde la app\.

# __10\. Asistente IA \(sobre el expediente\)__

Chat en lenguaje natural que responde con base en el expediente del paciente \(vitals, adherencia, observaciones, alertas, documentos\)\. El backend arma el contexto, llama al modelo LLM y persiste la conversación\. Soporta el punto de entrada “preguntar sobre esto” desde cualquier tarjeta de Salud mediante el campo context\_ref\. La respuesta puede entregarse por streaming \(SSE\) usando el mismo endpoint con Accept: text/event\-stream\.

### __10\.1 Preguntar al asistente__

__ POST   /api/v1/patients/\{patient\_id\}/assistant/messages__

Envía una pregunta del usuario\. Si no se pasa conversation\_id se crea una conversación nueva\. El asistente responde usando solo datos del expediente del paciente y siempre a los que el rol del usuario puede ver\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente sobre cuyo expediente se pregunta\.

conversation\_id

UUID | null

body

No

Conversación existente; null crea una nueva\.

text

str \(1–2000\)

body

Sí

Pregunta en lenguaje natural\.

context\_ref

ContextRef | null

body

No

Referencia de la tarjeta origen: \{kind: enum vital | medication | observation | alert | document, id: str\}\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

conversation\_id

UUID

Conversación\.

message\_id

UUID

Mensaje de respuesta\.

answer

str

Respuesta del asistente\.

sources

list\[SourceOut\]

Datos usados: \{kind, id, label\} para trazabilidad\.

created\_at

datetime

Fecha\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

429

ASSISTANT\_RATE\_LIMITED

Has hecho muchas preguntas seguidas\. Espera un momento\.

503

ASSISTANT\_UNAVAILABLE

El asistente no está disponible en este momento\. Intenta más tarde\.

### __10\.2 Listar conversaciones con el asistente__

__ GET   /api/v1/patients/\{patient\_id\}/assistant/conversations__

Historial de conversaciones del usuario con el asistente sobre este paciente\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ConversationOut\]

\{conversation\_id, title \(auto\-generado\), last\_message\_at, message\_count: int\}\.

### __10\.3 Historial de una conversación__

__ GET   /api/v1/assistant/conversations/\{conversation\_id\}/messages__

Mensajes de una conversación \(pregunta/respuesta\) en orden cronológico\.

__Roles autorizados: __Dueño de la conversación

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

conversation\_id

UUID

path

Sí

Conversación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[AssistantMsgOut\]

\{message\_id, sender: enum user | assistant, text, sources, created\_at\}\.

# __11\. Mensajes entre personas \(chat de coordinación\)__

Un canal de chat por paciente donde participan familiares, cuidadora y el adulto mayor\. Soporta texto, notas de voz y fotos; la entrega en tiempo real es por WebSocket con respaldo push\. La IA se puede invocar dentro del chat con @asistente: el backend detecta la mención, consulta el asistente \(sección 10\) y publica la respuesta como un mensaje más del canal\.

### __11\.1 Historial del chat__

__ GET   /api/v1/patients/\{patient\_id\}/chat/messages__

Mensajes del canal del paciente, paginados hacia atrás con cursor \(before\_id\) para scroll infinito\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente \(canal\)\.

before\_id

UUID | null

query

No

Cursor: mensajes anteriores a este id\.

limit

int \(1–100\)

query

No

Cantidad; por defecto 50\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ChatMessageOut\]

\{message\_id, sender: \{user\_id, full\_name, role\} | 'assistant', kind: enum text | voice | photo | assistant\_reply | system, text: str | null, media\_url: HttpUrl | null, duration\_sec: int | null, created\_at\}\.

has\_more

bool

Si hay mensajes más antiguos\.

### __11\.2 Enviar mensaje__

__ POST   /api/v1/patients/\{patient\_id\}/chat/messages__

Publica un mensaje de texto, nota de voz o foto en el canal\. Si el texto contiene @asistente, el backend genera además la respuesta de la IA como mensaje del canal\. El envío de fotos por parte de la cuidadora requiere plan Premium\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente \(canal\)\.

kind

enum: text | voice | photo

body

Sí

Tipo de mensaje\.

text

str \(1–2000\) | null

body

No\*

Texto \(\*obligatorio si kind=text\)\.

upload\_id

UUID | null

body

No\*

Media subida vía 8\.1 \(\*obligatorio si kind=voice o photo\)\.

duration\_sec

int | null

body

No

Duración de la nota de voz\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

message\_id

UUID

Mensaje creado\.

created\_at

datetime

Fecha\.

assistant\_reply\_id

UUID | null

Mensaje de la IA si hubo @asistente\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

402

PREMIUM\_REQUIRED

Enviar fotos al grupo familiar es una función Premium\.

400

EMPTY\_MESSAGE

El mensaje no puede estar vacío\.

### __11\.3 Canal en tiempo real__

__ GET   /ws/patients/\{patient\_id\}/chat  \(WebSocket\)__

Conexión WebSocket para recibir mensajes nuevos, confirmaciones de lectura e indicadores de escritura en tiempo real\. Autenticación por access token en el query param token\. Eventos del servidor: message\.new, message\.read, typing\. Si el cliente está desconectado, la entrega se respalda con push\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Canal del paciente\.

token

str \(JWT\)

query

Sí

Access token vigente\.

*Mensajes del servidor con el esquema \{event: str, data: ChatMessageOut | ReadReceipt | TypingEvent\}\. Cierre con código 4401 si el token es inválido y 4403 si no es miembro del paciente\.*

### __11\.4 Marcar mensajes como leídos__

__ POST   /api/v1/patients/\{patient\_id\}/chat/read__

Actualiza el puntero de lectura del usuario en el canal \(para badges de no leídos\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Canal\.

last\_read\_message\_id

UUID

body

Sí

Último mensaje leído\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

# __12\. Vista del adulto mayor: fotos y entretenimiento__

Soporte de backend para la vista de acompañamiento: galería de fotos curada por la familia con reacciones simples, y contenido de entretenimiento \(chistes y noticias\) curado, disponible en modo leer o escuchar\. La síntesis de voz \(TTS\) se resuelve con Azure AI Speech y se cachea el audio generado\. El chat del adulto mayor usa los mismos endpoints de la sección 11\.

### __12\.1 Compartir foto a la galería__

__ POST   /api/v1/patients/\{patient\_id\}/photos__

Un familiar publica una foto \(subida vía 8\.1\) en la galería del adulto mayor, con leyenda opcional\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

upload\_id

UUID

body

Sí

Foto subida\.

caption

str \(0–300\) | null

body

No

Leyenda\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

photo\_id

UUID

Foto publicada\.

created\_at

datetime

Fecha\.

### __12\.2 Galería de fotos__

__ GET   /api/v1/patients/\{patient\_id\}/photos__

Lista paginada de fotos de la galería, ordenadas de la más reciente a la más antigua\. Alimenta también el modo presentación \(slideshow\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

page / page\_size

int

query

No

Paginación \(por defecto 1 / 30\)\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[PhotoOut\]

\{photo\_id, photo\_url, caption, shared\_by: \{user\_id, full\_name\}, reactions: list\[ReactionOut\], created\_at\}\.

total

int

Total de fotos\.

### __12\.3 Reaccionar a una foto__

__ POST   /api/v1/photos/\{photo\_id\}/reactions__

El adulto mayor \(o un familiar\) reacciona con un corazón o una nota de voz\. La familia recibe la reacción como notificación amable \(no alerta\)\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

photo\_id

UUID

path

Sí

Foto\.

kind

enum: heart | voice

body

Sí

Tipo de reacción\.

upload\_id

UUID | null

body

No\*

Nota de voz subida \(\*obligatorio si kind=voice\)\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

reaction\_id

UUID

Reacción creada\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

ALREADY\_REACTED

Ya reaccionaste con un corazón a esta foto\.

### __12\.4 Eliminar foto de la galería__

__ DELETE   /api/v1/photos/\{photo\_id\}__

Quita una foto de la galería\. Solo quien la compartió o el familiar owner\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

photo\_id

UUID

path

Sí

Foto\.

__Respuesta exitosa: 204 No Content \(sin cuerpo\)\.__

### __12\.5 Contenido de entretenimiento \(chistes y noticias\)__

__ GET   /api/v1/content/feed__

Devuelve el feed curado del día: chistes y noticias apropiadas en tono ligero\. El contenido lo administra el equipo \(tabla content\_items alimentada por un proceso editorial/curaduría\)\. Cada ítem incluye, si existe, la URL del audio pregenerado para el modo escuchar\.

__Roles autorizados: __Adulto mayor, Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

kind

enum: joke | news | all

query

No

Filtro; por defecto all\.

limit

int \(1–50\)

query

No

Cantidad; por defecto 20\.

locale

str

query

No

Idioma del contenido; por defecto es\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ContentItemOut\]

\{content\_id, kind, title, body, source: str | null, audio\_url: HttpUrl | null, published\_at\}\.

### __12\.6 Sintetizar voz \(leer en voz alta\)__

__ POST   /api/v1/tts__

Convierte texto en audio \(Azure AI Speech\) para la lectura en voz alta de mensajes y contenido\. El audio se cachea por hash del texto para no re\-sintetizar\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

text

str \(1–3000\)

body

Sí

Texto a sintetizar\.

voice

str

body

No

Voz neural; por defecto es\-MX\-DaliaNeural\.

speed

float \(0\.5–1\.5\)

body

No

Velocidad de lectura; por defecto 0\.9 \(pausada\)\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

audio\_url

HttpUrl \(SAS\)

URL del audio MP3 generado \(exp\. 1 h\)\.

duration\_sec

int

Duración\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

503

TTS\_UNAVAILABLE

La lectura en voz alta no está disponible en este momento\.

### __12\.7 Transcribir voz a texto \(dictado\)__

__ POST   /api/v1/stt__

Transcribe una nota de voz \(subida vía 8\.1\) a texto para el modo dictado del adulto mayor\.

__Roles autorizados: __Familiar, Cuidadora, Médico, Adulto mayor

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

upload\_id

UUID

body

Sí

Audio subido \(m4a/ogg/wav, máx\. 5 MB\)\.

locale

str

body

No

Idioma; por defecto es\-MX\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

text

str

Transcripción\.

confidence

float \(0–1\)

Confianza de la transcripción\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

422

STT\_FAILED

No pudimos entender el audio\. Intenta de nuevo\.

# __13\. Vista de la cuidadora: check\-in, tareas, plan y trabajo__

Soporte de la operación diaria de la cuidadora: pantalla de check\-in del día, lista de tareas marcables, perfil profesional, y modelo freemium \(plan gratis/premium\)\. Las funciones premium se validan en backend con el estado de suscripción; las llamadas sin plan devuelven 402 PREMIUM\_REQUIRED con mensaje contextual para el upsell\.

### __13\.1 Check\-in del día \(pantalla principal\)__

__ GET   /api/v1/caregiver/today__

Agrega en una sola respuesta lo que la cuidadora necesita al abrir la app: paciente a cargo, estado general, próxima toma con cuenta regresiva, tareas del día y últimas notas de relevo\.

__Roles autorizados: __Cuidadora

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

patient

PatientCardOut

Adulto mayor a su cargo\.

wellbeing\_status

enum: ok | warning | attention

Estado general del día\.

next\_dose

DoseOut | null

Próxima toma de medicamento \(para la cuenta regresiva\)\.

tasks

list\[TaskOut\]

Tareas del día con su estado \(ver 13\.2\)\.

pending\_doses

int

Dosis pendientes de hoy\.

last\_handover

HandoverNoteOut | null

Última nota de relevo\.

active\_alerts

list\[AlertOut\]

Alertas activas del paciente\.

### __13\.2 Listar tareas del día__

__ GET   /api/v1/patients/\{patient\_id\}/tasks__

Tareas de cuidado de una fecha \(medicamentos, alimentación, higiene, actividad\)\. Las tareas de medicamentos se generan automáticamente del plan; las demás se crean manualmente o por plantilla diaria\.

__Roles autorizados: __Cuidadora, Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

date

date

query

No

Fecha; por defecto hoy\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[TaskOut\]

\{task\_id, category: enum medication | meal | hygiene | activity | other, title, scheduled\_at: datetime | null, status: enum pending | done | skipped, done\_by: UUID | null, done\_at: datetime | null\}\.

### __13\.3 Crear tarea__

__ POST   /api/v1/patients/\{patient\_id\}/tasks__

Agrega una tarea de cuidado al día \(única o recurrente diaria\)\.

__Roles autorizados: __Cuidadora, Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

patient\_id

UUID

path

Sí

Paciente\.

category

enum: meal | hygiene | activity | other

body

Sí

Categoría \(las de medicación se generan solas\)\.

title

str \(1–150\)

body

Sí

Descripción corta de la tarea\.

scheduled\_at

datetime | null

body

No

Hora sugerida\.

recurrence

enum: once | daily

body

No

Recurrencia; por defecto once\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

task\_id

UUID

Tarea creada\.

### __13\.4 Marcar tarea__

__ POST   /api/v1/tasks/\{task\_id\}/status__

Marca una tarea como realizada u omitida a medida que se cumple el día\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

task\_id

UUID

path

Sí

Tarea\.

status

enum: done | skipped | pending

body

Sí

Nuevo estado\.

note

str | null

body

No

Comentario opcional\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

task\_id

UUID

Tarea\.

status

enum

Estado resultante\.

### __13\.5 Mi perfil profesional__

__ GET   /api/v1/caregiver/profile__

Perfil profesional de la cuidadora: experiencia, especialidades, certificaciones y resumen de reseñas\. Es la base de su ficha en el marketplace\.

__Roles autorizados: __Cuidadora

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

profile\_id

UUID

Identificador\.

headline

str | null

Título profesional corto\.

bio

str | null

Presentación\.

years\_experience

int | null

Años de experiencia\.

specialties

list\[str\]

Especialidades \(ej\. demencia, movilidad reducida\)\.

languages

list\[str\]

Idiomas\.

zones

list\[str\]

Zonas de cobertura\.

certifications

list\[CertificationOut\]

\{name, issuer, year, document\_id: UUID | null\}\.

rating\_avg

float \(0–5\) | null

Calificación promedio\.

reviews\_count

int

Número de reseñas\.

is\_listed

bool

Visible en el marketplace\.

is\_featured

bool

Perfil destacado \(Premium\)\.

### __13\.6 Actualizar perfil profesional__

__ PUT   /api/v1/caregiver/profile__

Crea o actualiza el perfil profesional y su visibilidad en el marketplace\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

headline / bio / years\_experience / specialties / languages / zones / certifications

\(ver GET\)

body

No

Campos del perfil\.

is\_listed

bool

body

No

Publicar/despublicar en el marketplace\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(perfil\)

CaregiverProfileOut

Perfil actualizado\.

### __13\.7 Mi plan \(gratis/premium\)__

__ GET   /api/v1/caregiver/plan__

Estado de la suscripción de la cuidadora y catálogo de beneficios premium para la pantalla “Mi plan”\.

__Roles autorizados: __Cuidadora

*Entrada: sin parámetros \(solo token de autenticación\)\.*

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

plan

enum: free | premium

Plan vigente\.

valid\_until

datetime | null

Vencimiento del premium\.

benefits

list\[BenefitOut\]

\{code, name, included\_free: bool, included\_premium: bool\}\.

### __13\.8 Activar premium__

__ POST   /api/v1/caregiver/plan/upgrade__

Activa el plan premium validando el recibo de compra de la tienda \(Google Play / App Store\)\. El backend verifica el recibo con la tienda y activa la vigencia\.

__Roles autorizados: __Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

store

enum: google\_play | app\_store

body

Sí

Tienda de la compra\.

purchase\_token

str

body

Sí

Token/recibo de la compra in\-app\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

plan

enum

premium\.

valid\_until

datetime

Nueva vigencia\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

400

INVALID\_PURCHASE

No pudimos validar la compra\. Revisa tu método de pago e intenta de nuevo\.

409

ALREADY\_PREMIUM

Ya tienes un plan premium activo\.

### __13\.9 Ofertas de trabajo \(Premium\)__

__ GET   /api/v1/jobs__

Vitrina de ofertas de trabajo de cuidado publicadas en la plataforma\. El contacto ocurre fuera de la app\. Requiere plan premium\.

__Roles autorizados: __Cuidadora \(Premium\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

zone

str | null

query

No

Filtro por zona\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[JobOfferOut\]

\{job\_id, title, description, zone, schedule: str, pay\_range: str | null, contact\_info: str, published\_at\}\.

total

int

Total de ofertas\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

402

PREMIUM\_REQUIRED

Las ofertas de trabajo son una función Premium\. Mejora tu plan para verlas\.

### __13\.10 Historial y reportes extendidos \(Premium\)__

__ GET   /api/v1/caregiver/reports__

Estadísticas del trabajo de la cuidadora en un rango \(dosis administradas, adherencia lograda, observaciones registradas, tareas completadas\) y exportación en PDF\. Sin premium el historial se limita a los últimos 30 días\.

__Roles autorizados: __Cuidadora \(Premium\)

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

date\_from / date\_to

date

query

Sí

Rango del reporte\.

format

enum: json | pdf

query

No

Formato; por defecto json\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

stats

CaregiverStatsOut

\{doses\_given: int, adherence\_pct: float, observations: int, tasks\_done: int, incidents: int\}\.

daily

list\[DailyStatsOut\]

Serie diaria para gráficas\.

pdf\_url

HttpUrl | null

URL del PDF si format=pdf\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

402

PREMIUM\_REQUIRED

Los reportes extendidos son una función Premium\.

# __14\. Marketplace \(vitrina\)__

Vitrina de descubrimiento sin transacciones: búsqueda y comparación de cuidadoras y catálogo de artículos de apoyo\. El cierre \(contacto o compra\) ocurre fuera de la app, pero el backend registra los eventos de contacto para métricas y para preparar fases futuras \(agendar, contratar, pagar\)\.

### __14\.1 Buscar cuidadoras__

__ GET   /api/v1/marketplace/caregivers__

Listado con filtros de zona, especialidad, disponibilidad e idioma\. Las cuidadoras con perfil destacado \(Premium\) aparecen primero\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

q

str | null

query

No

Búsqueda por texto libre\.

zone

str | null

query

No

Zona de cobertura\.

specialty

str | null

query

No

Especialidad\.

language

str | null

query

No

Idioma\.

min\_rating

float \(0–5\) | null

query

No

Calificación mínima\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[CaregiverCardOut\]

\{profile\_id, full\_name, photo\_url, headline, years\_experience, specialties, zones, rating\_avg, reviews\_count, is\_featured\}\.

total

int

Resultados totales\.

### __14\.2 Perfil público de cuidadora__

__ GET   /api/v1/marketplace/caregivers/\{profile\_id\}__

Ficha completa: experiencia, especialidades, certificaciones y reseñas con calificaciones\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

profile\_id

UUID

path

Sí

Perfil\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

\(perfil\)

CaregiverPublicOut

Todos los campos públicos del perfil \(ver 13\.5\) sin datos de contacto directos\.

reviews

list\[ReviewOut\]

\{review\_id, rating: int 1–5, comment, author\_name, created\_at\}\.

### __14\.3 Contactar cuidadora__

__ POST   /api/v1/marketplace/caregivers/\{profile\_id\}/contact__

Registra la intención de contacto y devuelve los datos/canal de contacto definidos por la cuidadora\. La cuidadora recibe notificación del interés\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

profile\_id

UUID

path

Sí

Perfil a contactar\.

message

str \(0–500\) | null

body

No

Mensaje inicial opcional\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

contact\_channel

enum: phone | whatsapp | email

Canal preferido de la cuidadora\.

contact\_value

str

Teléfono o correo de contacto\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

409

CONTACT\_ALREADY\_SENT

Ya enviaste una solicitud de contacto a esta cuidadora hoy\.

### __14\.4 Calificar cuidadora__

__ POST   /api/v1/marketplace/caregivers/\{profile\_id\}/reviews__

Un familiar deja reseña y calificación\. Solo un familiar que tuvo a la cuidadora en su círculo de cuidado puede reseñar, una vez\.

__Roles autorizados: __Familiar

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

profile\_id

UUID

path

Sí

Perfil reseñado\.

rating

int \(1–5\)

body

Sí

Calificación\.

comment

str \(0–1000\) | null

body

No

Comentario\.

__Respuesta exitosa \(201 Created\):__

__Campo__

__Tipo__

__Descripción__

review\_id

UUID

Reseña creada\.

__Errores específicos \(además de los comunes de la sección 2\.5\):__

__HTTP__

__Código interno__

__Mensaje__

403

REVIEW\_NOT\_ALLOWED

Solo puedes reseñar a cuidadoras que hayan trabajado contigo\.

409

ALREADY\_REVIEWED

Ya dejaste una reseña para esta cuidadora\.

### __14\.5 Catálogo de artículos de apoyo__

__ GET   /api/v1/marketplace/products__

Catálogo navegable por categoría \(movilidad, monitoreo, seguridad en el hogar, cuidado diario\)\.

__Roles autorizados: __Familiar, Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

category

enum: mobility | monitoring | home\_safety | daily\_care | null

query

No

Filtro por categoría\.

q

str | null

query

No

Búsqueda por texto\.

page / page\_size

int

query

No

Paginación\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

items

list\[ProductCardOut\]

\{product\_id, name, category, thumbnail\_url, price\_range: str\}\.

total

int

Resultados totales\.

### __14\.6 Ficha de producto__

__ GET   /api/v1/marketplace/products/\{product\_id\}__

Detalle del artículo: descripción, fotos, rango de precio referencial y enlace externo para adquirirlo\.

__Roles autorizados: __Familiar, Cuidadora

__Parámetros de entrada:__

__Campo__

__Tipo__

__Origen__

__Oblig\.__

__Descripción__

product\_id

UUID

path

Sí

Producto\.

__Respuesta exitosa \(200 OK\):__

__Campo__

__Tipo__

__Descripción__

product\_id

UUID

Identificador\.

name

str

Nombre\.

category

enum

Categoría\.

description

str

Descripción\.

photos

list\[HttpUrl\]

Fotos\.

price\_range

str

Rango de precio referencial\.

external\_url

HttpUrl | null

Enlace a sitio externo para adquirir\.

contact\_info

str | null

Contacto del proveedor\.

# __15\. Anexo A — Modelo de datos PostgreSQL__

Tablas principales para orientar la implementación\. Todas usan id UUID \(gen\_random\_uuid\(\)\) como clave primaria y columnas created\_at / updated\_at con timestamptz\. Los borrados son lógicos \(deleted\_at\) en recursos del expediente\.

__Tabla__

__Propósito__

__Columnas clave__

users

Cuentas de usuario\.

email \(unique\), password\_hash, full\_name, phone, avatar\_url, locale

refresh\_tokens

Sesiones \(rotación de refresh\)\.

user\_id FK, token\_hash, expires\_at, revoked\_at

push\_devices

Dispositivos para push\.

user\_id FK, push\_token, platform, is\_active

patients

Perfil del adulto mayor\.

full\_name, birth\_date, sex, photo\_url, conditions jsonb, timezone

patient\_members

Membresía y rol por paciente\.

patient\_id FK, user\_id FK, role, is\_owner, UNIQUE\(patient\_id, user\_id\)

invitations

Invitaciones al círculo de cuidado\.

patient\_id FK, email, role, token\_hash, expires\_at, accepted\_by

wearables

Wearable vinculado\.

patient\_id FK, serial\_number \(unique\), model, battery\_pct, last\_sync\_at

vital\_readings

Lecturas de vitals \(particionada por mes\)\.

patient\_id FK, type, value, value\_secondary, measured\_at, source \(wearable | manual\), meta jsonb; UNIQUE\(patient\_id, type, measured\_at, source\)

vital\_thresholds

Umbrales por vital\.

patient\_id FK, type, min\_value, max\_value, updated\_by; UNIQUE\(patient\_id, type\)

medications

Plan de medicamentos\.

patient\_id FK, name, dose, instructions, times jsonb, days\_of\_week jsonb, start\_date, end\_date, grace\_window\_min, prescribed\_by, discontinued\_at

scheduled\_doses

Dosis generadas por día\.

medication\_id FK, patient\_id FK, scheduled\_at, status, logged\_by, logged\_at, reason, postponed\_until

observations

Bitácora \(incluye check\-ins\)\.

patient\_id FK, author\_id FK, category, text, photo\_blob\_path

incidents

Incidentes registrados\.

patient\_id FK, author\_id FK, type, severity, occurred\_at, description

handover\_notes

Notas de relevo entre turnos\.

patient\_id FK, author\_id FK, text

elder\_checkins

Check\-in del adulto mayor\.

patient\_id FK, feeling, date; UNIQUE\(patient\_id, date\)

uploads

Archivos subidos a Blob\.

user\_id FK, purpose, blob\_path, content\_type, size\_bytes, status

documents

Repositorio de documentos médicos\.

patient\_id FK, upload\_id FK, title, category, doc\_date, uploaded\_by

alerts

Alertas generadas\.

patient\_id FK, type, severity, title, detail, payload jsonb, status, acknowledged\_by, resolved\_at, resolution\_note

notification\_settings

Preferencias push por usuario\.

user\_id FK, alert\_type, push\_enabled; UNIQUE\(user\_id, alert\_type\)

assistant\_conversations

Conversaciones con la IA\.

patient\_id FK, user\_id FK, title

assistant\_messages

Mensajes IA \(pregunta/respuesta\)\.

conversation\_id FK, sender, text, sources jsonb

chat\_messages

Chat humano por paciente\.

patient\_id FK, sender\_id FK \(null si IA\), kind, text, media\_blob\_path, duration\_sec

chat\_read\_pointers

Puntero de lectura por usuario\.

patient\_id FK, user\_id FK, last\_read\_message\_id

photos

Galería del adulto mayor\.

patient\_id FK, upload\_id FK, shared\_by FK, caption

photo\_reactions

Reacciones a fotos\.

photo\_id FK, user\_id FK, kind, voice\_blob\_path; UNIQUE parcial \(photo\_id, user\_id\) para kind=heart

content\_items

Chistes y noticias curados\.

kind, title, body, source, audio\_blob\_path, locale, published\_at, is\_active

care\_tasks

Tareas del día\.

patient\_id FK, category, title, scheduled\_at, recurrence, status, done\_by, done\_at, task\_date

sos\_events

Eventos SOS\.

patient\_id FK, triggered\_by FK, note, alert\_id FK

caregiver\_profiles

Perfil profesional\.

user\_id FK \(unique\), headline, bio, years\_experience, specialties jsonb, languages jsonb, zones jsonb, certifications jsonb, is\_listed, is\_featured, rating\_avg, reviews\_count

caregiver\_subscriptions

Plan premium\.

user\_id FK, plan, store, purchase\_token, valid\_until

job\_offers

Ofertas de trabajo\.

title, description, zone, schedule, pay\_range, contact\_info, is\_active

marketplace\_products

Artículos de apoyo\.

name, category, description, photos jsonb, price\_range, external\_url, contact\_info, is\_active

caregiver\_reviews

Reseñas de cuidadoras\.

profile\_id FK, author\_id FK, rating, comment; UNIQUE\(profile\_id, author\_id\)

contact\_requests

Intenciones de contacto \(marketplace\)\.

profile\_id FK, family\_user\_id FK, message

## __15\.1 Índices recomendados__

- vital\_readings \(patient\_id, type, measured\_at DESC\): consultas de series y últimos valores\.
- scheduled\_doses \(patient\_id, scheduled\_at\) y \(status, scheduled\_at\) para el job de ventanas vencidas\.
- alerts \(patient\_id, status, created\_at DESC\) y chat\_messages \(patient\_id, created\_at DESC\)\.
- observations \(patient\_id, created\_at DESC\) y documents \(patient\_id, category\)\.

# __16\. Anexo B — Consideraciones de implementación__

## __16\.1 Procesos en segundo plano \(no son endpoints\)__

- Generador de dosis: crea las scheduled\_doses del día siguiente a partir del plan de medicamentos \(job nocturno por zona horaria del paciente\)\.
- Vigilante de ventanas: marca como missed las dosis no confirmadas al vencer scheduled\_at \+ grace\_window\_min y genera la alerta missed\_dose\.
- Vigilante de wearable: genera alerta wearable\_offline cuando last\_sync\_at supera la ventana de datos \(2 h\)\.
- Recordatorios de medicación: push a la cuidadora a la hora de cada dosis, persistente hasta confirmación\.
- Cálculo del semáforo: se materializa al vuelo en 5\.7; si el volumen crece, precalcular por paciente cada 15 minutos\.

## __16\.2 Seguridad y datos de salud__

- Cifrado en tránsito \(TLS 1\.2\+\) y en reposo \(nativo en Azure PostgreSQL y Blob\)\. Secretos en Azure Key Vault\.
- Autorización por membresía en cada endpoint \(dependencia FastAPI reutilizable get\_patient\_member\(role\_required\)\)\.
- Auditoría: bitácora de acceso a datos clínicos \(quién consultó qué expediente y cuándo\)\.
- Privacidad regional pendiente de definición legal \(pregunta abierta del documento de funcionalidades\); el diseño con borrado lógico y consentimiento por invitación facilita la adaptación\.

## __16\.3 Resumen de endpoints__

El documento define 82 endpoints agrupados en 12 módulos, además del canal WebSocket de chat\. Los módulos de salud y alertas \(secciones 4 a 9\) constituyen el camino crítico de la v1 y se recomienda implementarlos primero, seguidos de comunicación \(10–12\) y finalmente cuidadora/marketplace \(13–14\)\.
