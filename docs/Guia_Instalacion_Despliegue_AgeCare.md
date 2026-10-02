__Guía de Instalación y Despliegue__

AgeCare — Suite de cuidado de adultos mayores

*Entornos, variables de configuración y dependencias externas \(v1\)*

Fecha: 14 de agosto de 2026

Fuentes: agecare\_app/README\.md · pubspec\.yaml · AgeCare\_Especificacion\_Endpoints\_Backend\_v1

# 1\. Alcance de esta guía

AgeCare está compuesto por tres frentes: la app Flutter \(agecare\_app\), el backend \(FastAPI\) y el panel de administración web\. De estos tres, solo la app Flutter tiene código fuente entregado; el backend y el panel web existen únicamente como especificación \(ver Especificación de Endpoints Backend v1\)\.

Por eso esta guía tiene dos partes de naturaleza distinta:

- Sección 2 — App Flutter: instrucciones verificadas contra el código y el README reales del proyecto\. Se puede seguir literalmente hoy\.
- Secciones 3 y 4 — Backend y Web Admin: una plantilla con la arquitectura objetivo ya definida en la Especificación de Endpoints, marcada explícitamente como pendiente\. Sirve de punto de partida para que el equipo BE/WEB la complete con los pasos reales una vez exista el código, no como una guía ya operativa\.

# 2\. App Flutter \(agecare\_app\)

## 2\.1 Requisitos previos

- Flutter SDK con Dart >=3\.4\.0 <4\.0\.0 \(según environment\.sdk de pubspec\.yaml\)\.
- Xcode \(para build iOS\) y/o Android Studio con SDK de Android configurado \(para build Android\)\.
- Cuenta de Firebase con el proyecto AgeCare configurado, para notificaciones push \(ver sección 2\.5\)\.
- Acceso a las credenciales de Spike API \(SPIKE\_APP\_ID\) si se va a probar la integración real de wearables; no es necesario para el modo demo\.

## 2\.2 Entornos

__Entorno__

__Cuándo usarlo__

__Cómo se activa__

Demo / mock

Revisar UI y flujos sin backend\. Es el modo por defecto si no se pasa ninguna variable\.

USE\_MOCKS=true \(o no pasar nada\)

Desarrollo \(backend real\)

Probar contra el backend FastAPI una vez exista, en su entorno de desarrollo\.

USE\_MOCKS=false \+ API\_BASE\_URL apuntando al backend de desarrollo

Producción

Build de tienda \(App Store / Google Play\)\.

USE\_MOCKS=false \+ API\_BASE\_URL de producción \+ credenciales nativas reales \(sección 2\.6\)

## 2\.3 Instalación y ejecución

Pasos para levantar la app en modo demo \(sin backend\):

flutter pub get

flutter run \-\-dart\-define=USE\_MOCKS=true

Usuario de prueba en modo demo: demo@agecare\.app / agecare123 \(definido en el repositorio Mock de autenticación; no es una credencial real\)\.

Pasos para ejecutar contra el backend real \(cuando exista\) y Spike real:

flutter run \\

  \-\-dart\-define=USE\_MOCKS=false \\

  \-\-dart\-define=API\_BASE\_URL=https://api\-dev\.agecare\.app \\

  \-\-dart\-define=SPIKE\_APP\_ID=1234

## 2\.4 Variables de configuración

Definidas en lib/core/config/app\_config\.dart, se controlan por \-\-dart\-define en tiempo de compilación \(no hay archivo \.env en la app\):

__Variable__

__Tipo__

__Valor por defecto__

__Descripción__

USE\_MOCKS

bool

true

Si es true, usa repositorios en memoria con datos demo; no requiere backend\.

API\_BASE\_URL

String

https://api\-dev\.agecare\.app

URL base del backend real\. Se le agrega el sufijo /api/v1 automáticamente\.

SPIKE\_APP\_ID

int

0

Application ID de Spike API para la integración real de wearables\.

USE\_WEARABLE\_SIMULATOR

bool

true

Si es true, usa un simulador de wearable en vez del SDK real de Spike\. Es el valor por defecto mientras no haya SPIKE\_APP\_ID\.

## 2\.5 Dependencias externas y servicios de terceros

Servicios que la app espera tener disponibles para funcionar más allá del modo demo, según pubspec\.yaml y el README:

__Servicio__

__Para qué se usa__

__Dónde se configura__

Backend AgeCare \(FastAPI\)

Toda la persistencia y lógica de negocio real \(pacientes, vitals, medicamentos, alertas, chat, etc\.\)\.

Variable API\_BASE\_URL

Spike API \(spike\_flutter\_sdk\)

Integración de wearables \(HealthKit, Health Connect, Garmin, Whoop\)\.

Variable SPIKE\_APP\_ID; credenciales firmadas emitidas por el backend en POST /patients/\{id\}/wearable

Firebase / FCM

Notificaciones push remotas\.

GoogleService\-Info\.plist \(iOS\) / google\-services\.json \(Android\); el token se registra en el backend vía POST /users/me/devices

Azure Notification Hubs

Distribución de push detrás de FCM/APNs\.

Se configura del lado del backend, no en la app

App Store Connect / Google Play Console

Producto de compra in\-app agecare\_premium\_monthly \(premium de la cuidadora\)\.

Configuración de IAP en cada consola de tienda

## 2\.6 Configuración nativa pendiente por plataforma

Pasos que no son código Dart y se realizan al preparar los builds de tienda \(documentados en el README del proyecto\):

- iOS: capacidades de HealthKit y notificaciones; claves NSHealthShareUsageDescription, NSMicrophoneUsageDescription, NSLocationWhenInUseUsageDescription, NSCameraUsageDescription, NSPhotoLibraryUsageDescription en Info\.plist\.
- Android: permisos de Health Connect, POST\_NOTIFICATIONS, RECORD\_AUDIO, ACCESS\_FINE\_LOCATION, CAMERA; minSdk acorde a los requisitos de Health Connect\.
- Firebase: archivos de configuración GoogleService\-Info\.plist / google\-services\.json\.
- Spike: SPIKE\_APP\_ID y credenciales firmadas emitidas por el backend\.
- IAP: producto agecare\_premium\_monthly dado de alta en App Store Connect y Google Play Console\.

## 2\.7 Build de release \(referencial\)

El repositorio no documenta aún un proceso de build de release formal \(ni script, ni pipeline\)\. Los siguientes son los comandos estándar de Flutter para generar los artefactos de tienda; se incluyen como punto de partida y deben validarse con el flujo de firma/signing real que defina el equipo antes de usarse en producción:

flutter build appbundle \-\-dart\-define=USE\_MOCKS=false \-\-dart\-define=API\_BASE\_URL=<url\_prod>

flutter build ipa \-\-dart\-define=USE\_MOCKS=false \-\-dart\-define=API\_BASE\_URL=<url\_prod>

__Nota: __Conviene agregar una verificación automatizada que impida compilar un build de distribución sin USE\_MOCKS=false explícito, para evitar publicar accidentalmente en modo demo\.

# 3\. Backend \(FastAPI\) — plantilla pendiente de completar

__Pendiente de implementación: __no existe código de backend aún\. Lo que sigue es la arquitectura objetivo tal como la describe la Especificación de Endpoints Backend v1 \(sección 1\.1\), no una guía verificada contra una implementación real\. El equipo debe reemplazar cada punto por los pasos y valores reales una vez exista el repositorio\.

## 3\.1 Stack objetivo

__Componente__

__Tecnología prevista__

API

FastAPI \(Python 3\.12\) \+ Pydantic v2, desplegada en Azure App Service o Container Apps\.

Base de datos

Azure Database for PostgreSQL \(Flexible Server\), SQLAlchemy 2 async \+ asyncpg, migraciones con Alembic\.

Archivos

Azure Blob Storage con URLs firmadas \(SAS\)\.

Push

Azure Notification Hubs \(o FCM/APNs directo\)\.

IA

LLM para el asistente; Azure AI Speech \(TTS/STT\); Azure AI Document Intelligence \(OCR de recetas\)\.

Tiempo real

WebSocket nativo de FastAPI para el chat\.

Tareas programadas

Worker \(Celery/APScheduler \+ Azure Service Bus o cron\) para dosis diarias, ventanas de medicación vencidas, wearable sin datos y recordatorios\.

## 3\.2 Variables de entorno esperadas \(a definir por el equipo BE\)

La especificación no define nombres literales de variables de entorno; esta tabla traduce cada dependencia del stack a la variable que previsiblemente necesitará, como punto de partida para el equipo BE:

__Variable sugerida__

__Propósito__

DATABASE\_URL

Cadena de conexión a PostgreSQL \(Azure Database for PostgreSQL\)\.

AZURE\_STORAGE\_CONNECTION\_STRING

Acceso a Blob Storage para generar URLs firmadas \(SAS\)\.

AZURE\_KEY\_VAULT\_URL

Origen de secretos en tiempo de ejecución \(mencionado en la sección de seguridad 16\.2\)\.

NOTIFICATION\_HUB\_CONNECTION\_STRING

Envío de push vía Azure Notification Hubs\.

JWT\_SECRET / JWT\_ISSUER

Firma y validación de tokens de sesión\.

LLM\_API\_KEY

Acceso al proveedor de LLM del asistente IA\.

AZURE\_SPEECH\_KEY

Azure AI Speech para TTS/STT\.

AZURE\_DOC\_INTELLIGENCE\_KEY

Azure AI Document Intelligence para OCR de recetas\.

## 3\.3 Pasos de instalación \(a completar\)

Placeholder para que el equipo BE documente, cuando exista el repositorio: gestor de dependencias \(poetry/pip \+ requirements\.txt\), comando de migración \(alembic upgrade head\), comando de arranque local \(uvicorn\), y variables mínimas para levantar el entorno de desarrollo\. Se sugiere seguir el mismo formato de esta guía \(requisitos → entornos → instalación → variables → dependencias externas\) para mantener consistencia entre los tres frentes\.

# 4\. Panel de administración web — plantilla pendiente de completar

__Pendiente de implementación: __tampoco existe código del panel de administración web\. La Especificación de Endpoints Backend v1 no detalla su stack de frontend \(framework, hosting\) más allá de mencionarlo como épica EP\-13 del Plan de Desarrollo\. Esta sección queda como placeholder hasta que el equipo WEB defina y documente su propio stack, entorno y variables\.

# 5\. Resumen de estado

__Frente__

__Guía de instalación / despliegue__

App Flutter \(agecare\_app\)

Completa — secciones 2\.1 a 2\.7 de este documento, verificadas contra README\.md y pubspec\.yaml\.

Backend \(FastAPI\)

Pendiente — solo plantilla de arquitectura objetivo \(sección 3\), sin código que verificar todavía\.

Panel Web de administración

Pendiente — sin stack definido ni código \(sección 4\)\.
