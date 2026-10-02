__AgeCare — Suite de Cuidado de Adultos Mayores__

__Plan de Desarrollo — Versión 1__

10 sprints semanales · Equipo de 4 \+ refuerzo · Piloto y publicación en tiendas

Rol: Scrum Master

Fecha: 15 de julio de 2026

*Basado en: Documento de Funcionalidades v1, Wireframes v1 y Especificación de Endpoints Backend v1*

# __Contenido__

[__Contenido	2__](#_heading=)

[__1\. Resumen ejecutivo y supuestos	3__](#_heading=)

[1\.1 Supuestos	3](#_heading=)

[1\.2 Hitos	3](#_heading=)

[__2\. Equipo, capacidad y forma de trabajo	3__](#_heading=)

[2\.1 Equipo	3](#_heading=)

[2\.2 Capacidad	4](#_heading=)

[2\.3 Ceremonias	4](#_heading=)

[2\.4 Definition of Ready y Definition of Done	4](#_heading=)

[__3\. Epics	4__](#_heading=)

[__4\. Calendario de sprints \(roadmap\)	5__](#_heading=)

[__5\. Backlog detallado por sprint	7__](#_heading=)

[Sprint 1 \(Semana 1\) — Fundaciones	7](#_heading=)

[Sprint 2 \(Semana 2\) — Pacientes y onboarding	8](#_heading=)

[Sprint 3 \(Semana 3\) — Vitals, wearable y semáforo	10](#_heading=)

[Sprint 4 \(Semana 4\) — Medicamentos y adherencia	11](#_heading=)

[Sprint 5 \(Semana 5\) — Alertas, push y SOS \(pilar central\)	13](#_heading=)

[Sprint 6 \(Semana 6\) — Bitácora, documentos y check\-in de la cuidadora	14](#_heading=)

[Sprint 7 \(Semana 7\) — Chat en la app y asistente IA	16](#_heading=)

[Sprint 8 \(Semana 8\) — Vista del adulto mayor y arranque del piloto	17](#_heading=)

[Sprint 9 \(Semana 9\) — Marketplace en la app, premium y feedback del piloto	19](#_heading=)

[Sprint 10 \(Semana 10\) — Estabilización y envío a tiendas	20](#_heading=)

[__6\. Gestión de riesgos	22__](#_heading=)

[__7\. Estrategia de calidad	22__](#_heading=)

[__8\. Plan de release	22__](#_heading=)

[8\.1 Piloto \(semana 8\)	22](#_heading=)

[8\.2 Tiendas \(semana 10\)	22](#_heading=)

[8\.3 Línea de corte \(si el plan se atrasa\)	23](#_heading=)

# __1\. Resumen ejecutivo y supuestos__

Este plan lleva la versión 1 completa de AgeCare desde cero hasta el envío a App Store y Google Play en 10 semanas \(2\.5 meses\), con un piloto con usuarios reales a partir de la semana 8\. El alcance cubre todo el documento de funcionalidades v1: monitoreo de salud, alertas, medicamentos, comunicación \(chat \+ asistente IA\), vista del adulto mayor, vista de la cuidadora con freemium, marketplace vitrina y web de administración\.

__Advertencia del Scrum Master: es un plan agresivo\. La capacidad total es de ~180 días\-persona para un alcance que normalmente pediría 230–260\. El plan es viable solo si se cumplen los supuestos de abajo y se respeta la línea de corte de la sección 8\.3 cuando algo se atrase\. La publicación efectiva en tiendas depende de la revisión de Apple/Google \(3–7 días hábiles típicos\), que ocurre después de la semana 10\.__

## __1\.1 Supuestos__

- El backend FastAPI y la base de datos PostgreSQL los construye la persona de BD \(rol BE\), siguiendo la Especificación de Endpoints Backend v1 ya elaborada — esa especificación es el contrato entre frentes y permite trabajo en paralelo con mocks\.
- El refuerzo de app \(APP\-R\) está disponible al 50% desde el Sprint 1\. Sin este refuerzo, el plan no cierra: aplicar línea de corte de inmediato\.
- Wearable: en v1 se integra un simulador con interfaz desacoplada \(los datos entran por la API de ingesta batch\)\. La integración con el SDK del fabricante real es fase 2; si el dispositivo se define durante el proyecto, sustituye al simulador en el Sprint 9 con el buffer del refuerzo\.
- Las cuentas de desarrollador de Apple y Google existen o se tramitan en la semana 1 \(ticket AGE\-107\); el enrolamiento de Apple puede tardar días y es bloqueante para la semana 10\.
- Servicios Azure disponibles con presupuesto aprobado: PostgreSQL Flexible, Container Apps, Blob, Notification Hubs, Communication Services, AI Speech, AI Document Intelligence y acceso a un LLM \(Azure OpenAI o Claude API\)\.
- El equipo trabaja tiempo completo; los días estimados son días ideales de una jornada con ~20% ya descontado para ceremonias, revisiones de código y soporte\.

## __1\.2 Hitos__

__Semana__

__Hito__

__Criterio de éxito__

S1

Fundaciones listas

Registro/login desde la app contra API en Azure; CI/CD en los 3 frentes\.

S5

Núcleo de salud completo

Vitals \+ medicamentos \+ alertas push \+ SOS funcionando de punta a punta\.

S8

Inicio del piloto

RC distribuido a 15–25 usuarios reales por TestFlight/Play interno\.

S9

Congelación de alcance

Todo el alcance v1 implementado; solo correcciones desde aquí\.

S10

Envío a tiendas

Submission a App Store y Google Play con fichas y privacidad completas\.

S10\+

Publicación

Sujeta a revisión de tiendas; contingencia de rechazo en la sección 8\.

# __2\. Equipo, capacidad y forma de trabajo__

## __2\.1 Equipo__

__Código__

__Rol__

__Dedicación__

__Responsabilidad__

APP

Dev App \(Flutter\)

100%

App iOS/Android: todas las vistas \(familiar, cuidadora, adulto mayor\), integraciones nativas\.

APP\-R

Refuerzo App

50%

Firma/builds, alarmas, audio/voz, pantallas secundarias, correcciones piloto, submission\.

BE

Dev Backend \+ BD

100%

FastAPI, PostgreSQL, Azure, jobs, push, IA, seguridad\. Sigue la Especificación de Endpoints v1\.

WEB

Dev Web Admin

100%

Panel de administración: soporte, curación de contenido, catálogos, moderación, dashboards\.

QA

QA

100%

Plan de pruebas, automatización API, E2E en dispositivos, gestión del piloto, cumplimiento de tiendas\.

## __2\.2 Capacidad__

Sprints de 1 semana \(lunes a viernes\)\. Capacidad efectiva por sprint: APP 4 días, APP\-R 2, BE 4, WEB 4, QA 4 = 18 días\-persona por sprint, 180 en total\. Cada sprint de este plan asigna ≤18 días; los tickets de “bolsa de correcciones” \(sprints 9–10\) absorben lo imprevisto\.

## __2\.3 Ceremonias__

- Planning: lunes 9:00, 45 min\. Se confirma el sprint contra este plan y se ajusta con lo aprendido\.
- Daily: 15 min\. Foco en bloqueos entre frentes \(la dependencia API↔app es el riesgo diario número 1\)\.
- Review \+ demo: viernes, 45 min, con el hito demo de cada sprint\. Retro: 30 min a continuación\.
- Refinamiento: miércoles, 30 min, mirando el sprint siguiente\.

## __2\.4 Definition of Ready y Definition of Done__

- DoR: el ticket tiene criterios de aceptación, dependencias resueltas o mockeables, y diseño/wireframe de referencia si es UI\.
- DoD: código revisado \(PR aprobado\), pruebas automatizadas donde aplique, criterios de aceptación verificados por QA, desplegado en dev, sin regresiones conocidas y documentación mínima actualizada\.

# __3\. Epics__

Priorización MoSCoW pensada para la línea de corte: si el plan se atrasa, se recorta desde Could hacia Should sin tocar los Must\.

__Epic__

__Nombre__

__Prioridad__

__Sprints__

__Alcance__

EP\-01

Fundaciones e infraestructura

Must

S1

Azure, CI/CD, esqueletos de API, app y web admin\.

EP\-02

Autenticación y cuentas

Must

S1–S2

Registro, login, JWT, recuperación, dispositivos push\.

EP\-03

Pacientes, roles y onboarding

Must

S2

Perfil de paciente, invitaciones, círculo de cuidado, multi\-paciente\.

EP\-04

Vitals, wearable y semáforo

Must

S3

Ingesta batch, series, umbrales, semáforo del día, simulador wearable\.

EP\-05

Medicamentos y adherencia

Must

S4

Plan, dosis, alarmas, confirmación, adherencia, OCR de recetas\.

EP\-06

Alertas, push y SOS

Must

S5

Motor de alertas, push, campana, flujo de caídas, SOS\.

EP\-07

Bitácora y documentos

Must

S6

Observaciones, incidentes, relevo, check\-in elder, documentos SAS\.

EP\-08

Chat de coordinación

Must

S6–S7

Mensajes texto/voz/foto, WebSocket, @asistente\.

EP\-09

Asistente IA

Should

S7

Chat sobre el expediente, fuentes, entrada contextual\.

EP\-10

Vista del adulto mayor

Should

S8

Mosaicos accesibles, voz primero, galería, entretenimiento\.

EP\-11

Cuidadora y freemium

Must/Should

S4–S9

Check\-in, tareas, SOS \(Must\); premium, perfil, ofertas, reportes \(Should\)\.

EP\-12

Marketplace vitrina

Could

S6, S8–S9

Búsqueda de cuidadoras, productos, contacto, reseñas\.

EP\-13

Web de administración

Must

S1–S10

Soporte, curación, catálogos, moderación, dashboards, legales\.

EP\-14

Calidad \(transversal\)

Must

S1–S10

Automatización, E2E, regresiones, gestión del piloto\.

EP\-15

Lanzamiento

Must

S8, S10

Piloto, fichas, privacidad, submission y revisión de tiendas\.

# __4\. Calendario de sprints \(roadmap\)__

__Sprint__

__Tema__

__APP / APP\-R__

__BE__

__WEB__

__QA__

S1

Fundaciones

Esqueleto \+ login/registro; firma y pipelines

Infra Azure, esqueleto API, auth

Esqueleto panel \+ login

Plan maestro, arnés API

S2

Onboarding

Crear paciente, invitaciones, navegación

Pacientes, invitaciones, push devices

Gestión usuarios

Casos \+ automatización onboarding

S3

Vitals

Salud con gráficas, Inicio con semáforo; simulador

Ingesta, series, umbrales, semáforo

Seeds demo, parámetros sistema

Automatización vitals, regresión

S4

Medicamentos

Plan, agenda de tomas, adherencia; alarmas

Plan, dosis, jobs, OCR

Expediente soporte, correos

E2E medicación, alarmas en dispositivos

S5

Alertas y SOS

Campana, flujo caída, SOS; ajustes notif\.

Motor alertas, push, SOS

Monitor alertas, CRUD contenido

E2E alertas en dispositivos

S6

Bitácora y chat BE

Check\-in cuidadora, observaciones; docs, relevo

Bitácora, uploads SAS, chat\+WS

Moderación, catálogo productos

Regresión medio término, arnés WS

S7

Comunicación

Chat completo, asistente IA; notas de voz

Asistente IA, @asistente, TTS/STT

Auditoría IA, ofertas trabajo

Pruebas IA y chat multi\-dispositivo

S8

Adulto mayor \+ RC

Vista elder, galería, entretenimiento; voz primero

Fotos, feed, marketplace API, IAP

Moderación marketplace, dashboard piloto

RC \+ arranque del piloto

S9

Cierre de alcance

Marketplace, premium IAP; perfil/ofertas, fixes

Reportes, hardening, fixes piloto

Suscripciones, mejoras piloto

IAP \+ triage piloto

S10

Release

Fixes finales, fichas; gestión de revisión

Carga, prod, soporte release

Manual, páginas legales

Regresión final, checklist tiendas

# __5\. Backlog detallado por sprint__

Se especifican 108 tickets\. Cada uno incluye descripción, criterios de aceptación \(✓\), rol asignado, estimación en días ideales y dependencias\. Los IDs referencian secciones de la Especificación de Endpoints Backend v1 cuando aplica\.

## __Sprint 1 \(Semana 1\) — Fundaciones__

Objetivo: infraestructura Azure operativa, esqueletos de los tres frentes \(API, app, web admin\) con CI/CD, y autenticación funcionando de punta a punta\.

__Demo: registro e inicio de sesión desde la app contra la API en Azure\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-101

__Aprovisionar infraestructura Azure__

Crear grupo de recursos con Azure Database for PostgreSQL \(Flexible Server\), Container Apps \(o App Service\), Blob Storage, Key Vault y Application Insights\. Entornos dev y prod\.

__✓ __Infra descrita como IaC \(Bicep/Terraform\) en el repo

__✓ __Conexión API↔BD con secretos en Key Vault

__✓ __Backups automáticos de BD activados

__BE__

1

—

AGE\-102

__Esqueleto FastAPI \+ CI/CD__

Proyecto FastAPI con estructura de routers por módulo, SQLAlchemy async, Alembic, formato estándar de error \(sección 2\.4 de la especificación\) y pipeline GitHub Actions \(lint, tests, deploy a dev\)\.

__✓ __Push a main despliega a dev automáticamente

__✓ __Healthcheck /health responde en Azure

__✓ __Manejador global de errores devuelve el JSON estándar

__BE__

1

101

AGE\-103

__Modelo de datos núcleo \+ migraciones__

Tablas users, refresh\_tokens, push\_devices, patients, patient\_members, invitations según el Anexo A de la especificación de endpoints\.

__✓ __Migración Alembic aplicable y reversible

__✓ __Constraints UNIQUE e índices del anexo creados

__BE__

1

102

AGE\-104

__API de autenticación__

Endpoints 3\.1–3\.4 \(register, login, refresh rotatorio, logout\) con JWT y hash argon2\. Recuperación de contraseña \(3\.5–3\.6\) se hace en Sprint 2\.

__✓ __Tests de integración de los 4 flujos

__✓ __Login devuelve memberships por paciente

__✓ __Refresh usado dos veces revoca la sesión

__BE__

1

103

AGE\-105

__Esqueleto Flutter \+ design system__

Proyecto Flutter con flavors \(dev/prod\), enrutamiento \(go\_router\), estado \(Riverpod/Bloc\), i18n es, cliente HTTP con interceptor de tokens, y design system base \(colores, tipografía, componentes\) según wireframes\.

__✓ __Compila en iOS y Android desde CI

__✓ __Tema y componentes base documentados en una pantalla galería

__✓ __Interceptor renueva el access token automáticamente

__APP__

2

—

AGE\-106

__Pantallas de registro e inicio de sesión__

Login, registro y estados de error conectados a la API real\. Persistencia segura de tokens \(Keychain/Keystore\)\.

__✓ __Flujo registro→login→home vacío funciona en ambos SO

__✓ __Errores de la API se muestran con su mensaje en español

__✓ __Sesión persiste al reiniciar la app

__APP__

2

104, 105

AGE\-107

__Firma y pipelines móviles__

Certificados iOS, keystore Android, fastlane para builds y distribución a TestFlight/Play interno\. Alta de cuentas de desarrollador si falta \(crítico para Sprint 10\)\.

__✓ __Build firmada distribuida a TestFlight y Play interno desde CI

__✓ __Cuentas App Store y Play verificadas y con acuerdos fiscales aceptados

__APP\-R__

2

105

AGE\-108

__Esqueleto web admin \+ login__

SPA React \(Vite \+ TypeScript\) con layout, rutas protegidas y login contra la API \(usuarios internos con rol admin en tabla aparte o claim\)\.

__✓ __Deploy automático a Azure Static Web Apps

__✓ __Login admin con JWT y expiración manejada

__WEB__

2\.5

104

AGE\-109

__Definición de roles internos y auditoría admin__

Modelo de permisos del panel \(admin, soporte, editor de contenido\) y registro de acciones administrativas\.

__✓ __Rutas del panel restringidas por rol

__✓ __Toda acción de escritura queda en bitácora de auditoría

__WEB__

1\.5

108

AGE\-110

__Plan maestro de pruebas y matriz de dispositivos__

Estrategia de pruebas \(niveles, herramientas, criterios de salida\), matriz iOS/Android \(versiones y tamaños\) y definición de severidades de bugs\.

__✓ __Documento aprobado por el equipo

__✓ __Matriz cubre iOS 16\+ y Android 10\+ en 6 dispositivos

__QA__

2

—

AGE\-111

__Entorno de pruebas de API automatizadas__

Framework de pruebas de API \(pytest \+ httpx o Postman/Newman\) corriendo en CI contra el entorno dev, con datos semilla\.

__✓ __Suite corre en cada PR

__✓ __Primeras pruebas de auth verdes \(con AGE\-104\)

__QA__

2

104

## __Sprint 2 \(Semana 2\) — Pacientes y onboarding__

Objetivo: el familiar crea el paciente, invita al círculo de cuidado y la app tiene su navegación completa con selector multi\-paciente\.

__Demo: onboarding completo familiar→paciente→invitación aceptada por cuidadora\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-201

__API de pacientes y membresías__

Endpoints 4\.1–4\.4 y 4\.7–4\.8 \(CRUD paciente, listar círculo, quitar miembro\) con dependencia reutilizable de autorización get\_patient\_member\(role\)\.

__✓ __403 con mensaje estándar si el rol no corresponde

__✓ __Owner no puede ser eliminado

__✓ __Tests de permisos por rol

__BE__

1\.5

104

AGE\-202

__API de invitaciones__

Endpoints 4\.5–4\.6: creación con token de un solo uso \(7 días\), correo vía Azure Communication Services, aceptación con y sin cuenta previa\.

__✓ __Token usado o vencido responde INVALID\_INVITATION

__✓ __Registro con invitation\_token crea la membresía correcta

__✓ __Correo de invitación llega con enlace profundo

__BE__

1\.5

201

AGE\-203

__Recuperación de contraseña \+ registro de dispositivos push__

Endpoints 3\.5, 3\.6 y 3\.9\. Correo de recuperación con token de 30 minutos\.

__✓ __Respuesta 202 uniforme exista o no el correo

__✓ __Reset revoca todas las sesiones

__✓ __push\_token duplicado actualiza en vez de duplicar

__BE__

1

104

AGE\-204

__Onboarding: crear perfil del paciente__

Flujo de alta del paciente \(datos, foto, padecimientos\) y pantalla vacía de bienvenida cuando no hay pacientes\.

__✓ __Paciente creado aparece en el selector

__✓ __Validaciones en línea con mensajes de la API

__APP__

1\.5

201

AGE\-205

__Flujo de invitaciones en la app__

Enviar invitación por rol, compartir enlace, y aceptación vía deep link \(app instalada\) o tras registro\.

__✓ __Deep link abre la app y acepta la invitación

__✓ __Invitado ve al paciente con la vista de su rol

__APP__

1\.5

202

AGE\-206

__Shell de navegación \+ selector de paciente__

Barra inferior de 5 entradas \(Inicio, Salud, Comunicación, Marketplace, Más\), selector de paciente y campana persistentes según wireframe familiar\.

__✓ __Cambiar paciente refresca todas las pestañas

__✓ __La vista mostrada depende del rol del usuario

__APP__

1

204

AGE\-207

__Pantalla Más: pacientes, roles e invitaciones__

Gestión desde la app: lista de pacientes, círculo de cuidado por paciente, invitaciones pendientes, reenviar/revocar\.

__✓ __Owner puede quitar miembros con confirmación

__✓ __Estados de invitación visibles \(pendiente/aceptada/vencida\)

__APP\-R__

2

205

AGE\-208

__Web admin: gestión de usuarios y pacientes__

Búsqueda y detalle de usuarios y pacientes para soporte: ver membresías, desactivar cuentas, reenviar invitaciones\.

__✓ __Búsqueda por nombre/correo con paginación

__✓ __Desactivar cuenta revoca sesiones y lo registra en auditoría

__WEB__

2\.5

201

AGE\-209

__Web admin: métricas básicas de adopción__

Tarjetas de conteo: usuarios por rol, pacientes activos, invitaciones aceptadas/pendientes\.

__✓ __Datos en vivo desde endpoints admin dedicados

__✓ __Carga en <2 s

__WEB__

1\.5

208

AGE\-210

__Casos de prueba de auth y onboarding__

Diseño y ejecución de casos manuales: registro, login, recuperación, invitaciones por rol, multi\-paciente, permisos\.

__✓ __Suite de casos en la herramienta de gestión \(mín\. 40 casos\)

__✓ __Ejecución completa con reporte de defectos

__QA__

2

205

AGE\-211

__Automatización API: pacientes e invitaciones__

Pruebas automatizadas de los endpoints de pacientes, membresías, invitaciones y matriz de permisos por rol\.

__✓ __Matriz rol×recurso cubierta \(16 combinaciones clave\)

__✓ __Verde en CI

__QA__

2

201, 202

## __Sprint 3 \(Semana 3\) — Vitals, wearable y semáforo__

Objetivo: datos de vitals fluyendo \(simulador de wearable \+ captura manual\), pantalla de Salud con tendencias y el semáforo del día en Inicio\.

__Demo: Inicio/Hoy con semáforo real calculado y gráficas de vitals\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-301

__API ingesta de vitals \(batch \+ manual\)__

Endpoints 5\.1–5\.2 con idempotencia por \(patient, type, measured\_at, source\), tabla particionada vital\_readings y vinculación de wearable \(4\.9–4\.10\)\.

__✓ __Lote de 500 lecturas <1 s

__✓ __Duplicados descartados sin error

__✓ __last\_sync\_at y batería se actualizan

__BE__

1\.5

201

AGE\-302

__API series, últimos valores y umbrales__

Endpoints 5\.3–5\.6: agregación raw/hora/día/semana en SQL, últimos valores por tipo y CRUD de umbrales\.

__✓ __Serie de 30 días agregada por día en <300 ms

__✓ __Umbral inválido responde INVALID\_THRESHOLD\_RANGE

__BE__

1\.5

301

AGE\-303

__API semáforo del día y tablero multi\-paciente__

Endpoints 5\.7–5\.8\. Regla v1 del semáforo: attention si hay alerta crítica activa o ≥2 señales \(vital fuera de rango, dosis omitida, sin datos de wearable\); warning con 1 señal; ok en otro caso\.

__✓ __Regla documentada en el repo y validada con casos de tabla

__✓ __status\_reasons legibles en español

__BE__

1

302

AGE\-304

__Pantalla Salud: tarjetas de vitals y tendencias__

Tarjetas por grupo de vitals \(ritmo, SpO2, sueño/actividad, caídas\) con valor actual, mini\-gráfica \(fl\_chart\), detalle con rango semanal/mensual y línea de umbral\.

__✓ __Coincide con wireframe Salud·Elena

__✓ __Cambio de rango 7/30/90 días fluido

__✓ __Estado de sincronización del wearable visible

__APP__

2\.5

302

AGE\-305

__Pantalla Inicio/Hoy con semáforo__

Semáforo del día, tarjetas resumen \(vitals, medicamentos de hoy, última observación\), banda de alertas activas \(placeholder hasta Sprint 5\) y tarjetas\-semáforo multi\-paciente\.

__✓ __Con 2\+ pacientes muestra tarjeta por cada uno

__✓ __Pull\-to\-refresh actualiza el resumen

__APP__

1\.5

303

AGE\-306

__Simulador de wearable e ingesta desde la app__

Módulo de ingesta que sube lotes a 5\.1: simulador configurable \(normal, SpO2 bajo, caída\) para desarrollo y demos, con interfaz para conectar el SDK real del wearable en fase 2\.

__✓ __Simulador genera 24 h de datos realistas por escenario

__✓ __Interfaz WearableSource desacoplada del proveedor

__APP\-R__

2

301

AGE\-307

__Web admin: semillas y datos demo__

Herramienta admin para poblar pacientes demo con historial de vitals, para QA y demos comerciales\.

__✓ __Un clic crea paciente demo con 30 días de datos

__✓ __Solo disponible en entornos no productivos

__WEB__

1\.5

301

AGE\-308

__Web admin: umbrales por defecto y parámetros del sistema__

Pantalla de configuración global: umbrales por defecto por vital, ventana de wearable sin datos, parámetros del semáforo\.

__✓ __Cambios auditados y aplicados a pacientes nuevos

__✓ __Validación de rangos en el formulario

__WEB__

2\.5

302

AGE\-309

__Automatización de vitals \+ generador de datos__

Pruebas de ingesta \(idempotencia, límites\), series y semáforo con datasets sintéticos por escenario\.

__✓ __Los 3 estados del semáforo reproducidos por datos

__✓ __Pruebas de carga básica: 50 lotes concurrentes

__QA__

2\.5

303

AGE\-310

__Regresión sprints 1–2 y pruebas exploratorias app__

Regresión de auth/onboarding sobre builds nuevas y exploratorias de la pantalla de Salud en la matriz de dispositivos\.

__✓ __Reporte de regresión sin bloqueantes abiertos

__QA__

1\.5

304

## __Sprint 4 \(Semana 4\) — Medicamentos y adherencia__

Objetivo: ciclo completo de medicación: plan → dosis generadas → alarma → confirmación → adherencia visible para el familiar\. OCR de recetas operativo\.

__Demo: dosis confirmada desde la alarma y adherencia reflejada en la vista del familiar\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-401

__API plan de medicamentos \+ generador de dosis__

Endpoints 6\.1–6\.4 y job nocturno que materializa scheduled\_doses por zona horaria del paciente\. Edición regenera solo dosis futuras\.

__✓ __Dosis del día siguiente generadas a las 00:00 locales

__✓ __Descontinuar cancela futuras y conserva historial

__BE__

1\.5

201

AGE\-402

__API registro de dosis y adherencia__

Endpoints 6\.5–6\.7 y job vigilante que marca missed al vencer la ventana y dispara la alerta \(se conecta al motor en Sprint 5\)\.

__✓ __Dosis ya registrada responde DOSE\_ALREADY\_LOGGED

__✓ __missed requiere motivo

__✓ __Adherencia calculada correctamente en casos de tabla

__BE__

1\.5

401

AGE\-403

__API OCR de recetas__

Endpoint 6\.8 con Azure AI Document Intelligence: sube receta, extrae medicamentos sugeridos con confianza, guarda el documento\.

__✓ __Receta legible produce ≥1 sugerencia con nombre y dosis

__✓ __Falla de OCR responde OCR\_FAILED con mensaje amable

__BE__

1

401

AGE\-404

__App cuidadora: alta y edición del plan__

Formulario de medicamento \(nombre, dosis, horarios, días, vigencia\) y flujo de importación por foto de receta con revisión de sugerencias\.

__✓ __Sugerencias OCR editables antes de confirmar

__✓ __Familiar ve el plan en solo lectura

__APP__

1\.5

401, 403

AGE\-405

__App cuidadora: agenda de tomas y confirmación__

Lista de dosis del día con estados, próxima toma con cuenta regresiva, y registro tomada/pospuesta/omitida con motivo\.

__✓ __Cuenta regresiva coincide con scheduled\_at local

__✓ __Posponer >4 h bloqueado con mensaje de la API

__APP__

1\.5

402

AGE\-406

__App familiar: vista de adherencia__

Tarjeta de medicamentos de hoy en Inicio \(tomadas/pendientes/omitidas\) y detalle de adherencia con porcentaje y desglose por medicamento\.

__✓ __Números cuadran con la API en datos demo

__✓ __Sin acciones de edición para el rol familiar

__APP__

1

402

AGE\-407

__Alarmas locales de medicación__

Notificaciones locales programadas por dosis para la cuidadora, persistentes hasta confirmar, con acciones rápidas \(tomada/posponer\) desde la notificación\.

__✓ __Alarma dispara con la app cerrada en iOS y Android

__✓ __Confirmar desde la notificación registra la dosis

__APP\-R__

2

405

AGE\-408

__Web admin: expediente de solo lectura para soporte__

Vista por paciente para el equipo de soporte: plan de medicamentos, dosis recientes, vitals y estado del wearable\.

__✓ __Acceso restringido a rol soporte y auditado

__✓ __Sin capacidad de edición clínica

__WEB__

2\.5

402

AGE\-409

__Web admin: alta de administradores y ajustes de correo__

Gestión de cuentas internas del panel y plantillas de correos transaccionales \(invitación, recuperación\)\.

__✓ __Plantillas editables con variables y vista previa

__WEB__

1\.5

109

AGE\-410

__Pruebas E2E de medicación__

Escenarios: plan multi\-horario, edición a mitad de tratamiento, ventana vencida→missed, posposición, adherencia\. Automatización API \+ manual en app\.

__✓ __12 escenarios E2E documentados y ejecutados

__✓ __Bug crítico de zona horaria descartado con paciente en otra TZ

__QA__

2\.5

405

AGE\-411

__Regresión sprint 3 y pruebas de alarmas en dispositivos__

Regresión de vitals/semáforo y verificación de alarmas locales en la matriz de dispositivos \(Doze mode, background refresh\)\.

__✓ __Alarmas verificadas en los 6 dispositivos de la matriz

__QA__

1\.5

407

## __Sprint 5 \(Semana 5\) — Alertas, push y SOS \(pilar central\)__

Objetivo: el pilar de alertas completo: motor en backend, push en dispositivos, centro de alertas con campana, flujo crítico de caídas y botón SOS\.

__Demo: caída simulada → push en el teléfono del familiar → flujo de acción inmediata\. Fin de la fase núcleo de salud\.__

*Carga del sprint: BE 3\.5d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-501

__Motor de alertas \+ push__

Servicio que evalúa lecturas \(umbral, fall\_event\), dosis vencidas y wearable sin datos; crea alerts y envía push vía Notification Hubs respetando notification\_settings\. Endpoints 9\.1–9\.3\.

__✓ __Caída genera alerta crítica y push en <10 s

__✓ __Alerta atendida detiene recordatorios

__✓ __Sin duplicados por la misma condición en 30 min

__BE__

2

301, 402

AGE\-502

__API preferencias de notificación__

Endpoints 9\.4–9\.5 con bloqueo de alertas críticas \(caída, SOS\)\.

__✓ __Desactivar crítica responde CRITICAL\_ALERT\_LOCKED

__BE__

0\.5

501

AGE\-503

__API SOS__

Endpoint 9\.6: alerta crítica, push a todos los familiares, registro en expediente y contactos de emergencia en la respuesta\.

__✓ __Evento queda en el expediente con hora

__✓ __Todos los familiares del paciente reciben push

__BE__

1

501

AGE\-504

__App: recepción de push y campana__

Integración FCM/APNs, badge de no leídas, centro de alertas con pestañas Activas/Historial según wireframe, atender y resolver con nota\.

__✓ __Push abre la alerta correcta \(deep link\)

__✓ __Badge consistente con unread\_count

__APP__

1\.5

501

AGE\-505

__App: flujo crítico de caída__

Pantalla de acción inmediata al recibir alerta de caída: llamar a la cuidadora, llamar a emergencias, marcar como atendida\. Banda de alertas activas en Inicio\.

__✓ __Flujo alcanzable desde push con app cerrada

__✓ __Botones de llamada abren el marcador con el número

__APP__

1\.5

504

AGE\-506

__App cuidadora: botón SOS__

Botón siempre visible en la vista cuidadora, confirmación anti\-toque accidental, nota opcional y pantalla con contactos de emergencia\.

__✓ __SOS visible en todas las pantallas de la vista cuidadora

__✓ __Confirmación en <2 toques

__APP__

1

503

AGE\-507

__App: configuración de notificaciones y umbrales__

Pantalla de ajustes: preferencias push por tipo y edición de umbrales por vital \(rol familiar/médico\)\.

__✓ __Críticas aparecen bloqueadas con explicación

__✓ __Umbral editado se refleja en las gráficas

__APP\-R__

2

502

AGE\-508

__Web admin: monitor global de alertas__

Tablero operativo: alertas críticas activas en la plataforma, tiempos de atención, filtros por tipo y fecha\.

__✓ __Vista se actualiza sola cada 60 s

__✓ __Exportable a CSV

__WEB__

2

501

AGE\-509

__Web admin: CRUD de contenido \(chistes y noticias\)__

Gestión de content\_items para el entretenimiento del adulto mayor: alta, edición, curaduría, programación de publicación y generación de audio TTS pregenerado\.

__✓ __Ítem publicado aparece en el feed \(API 12\.5\)

__✓ __Botón genera y adjunta el audio del ítem

__WEB__

2

109

AGE\-510

__E2E de alertas en dispositivos reales__

Matriz tipo de alerta × plataforma × estado de app \(primer plano, fondo, cerrada\)\. Verificación de latencia y deep links\.

__✓ __24 combinaciones ejecutadas y documentadas

__✓ __Latencia push <30 s en todos los casos

__QA__

2\.5

505

AGE\-511

__Pruebas de SOS y regresión de medicación__

E2E de SOS \(multi\-familiar\) y regresión del ciclo de medicación con las alertas ya conectadas\.

__✓ __Dosis omitida genera alerta al familiar en E2E completo

__QA__

1\.5

506

## __Sprint 6 \(Semana 6\) — Bitácora, documentos y check\-in de la cuidadora__

Objetivo: la cuidadora opera su día completo \(check\-in, tareas, observaciones, incidentes, relevo\) y el expediente guarda documentos\. Backend del chat listo\.

__Demo: jornada completa de la cuidadora capturada desde la app\.__

*Carga del sprint: BE 4d · APP 3\.5d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-601

__API bitácora: observaciones, incidentes, relevo y check\-in__

Endpoints 7\.1–7\.6\. Incidente crítico genera alerta vía el motor del Sprint 5\.

__✓ __Check\-in del adulto mayor limitado a 1/día

__✓ __Incidente critical dispara push al familiar

__BE__

1

501

AGE\-602

__API uploads SAS \+ documentos__

Endpoints 8\.1–8\.5: URLs firmadas de subida/descarga con Azure Blob, registro y listado de documentos\.

__✓ __Subida directa a Blob sin pasar por la API

__✓ __URL de descarga expira en 15 min

__BE__

1

101

AGE\-603

__API chat: mensajes, WebSocket y lecturas__

Endpoints 11\.1–11\.4: historial con cursor, envío \(texto/voz/foto\), canal WS por paciente con eventos message\.new/read/typing, y respaldo push a desconectados\.

__✓ __Mensaje llega por WS a 3 clientes conectados <1 s

__✓ __Cliente desconectado recibe push

__✓ __Cierre 4403 si no es miembro

__BE__

2

602

AGE\-604

__App cuidadora: check\-in del día y tareas__

Pantalla principal de la cuidadora según wireframe: encabezado con estado, próxima toma con cuenta regresiva, tareas marcables por categoría, acciones rápidas\. APIs 13\.1–13\.4\.

__✓ __Coincide con wireframe Hoy·turno mañana

__✓ __Tarea marcada actualiza el resumen sin recargar

__APP__

2

601

AGE\-605

__App: observaciones con foto e incidentes__

Captura de observación \(categoría, texto, foto\) e incidentes con hora y gravedad; bitácora visible para el familiar en Salud\.

__✓ __Foto se sube por SAS y aparece en la bitácora

__✓ __Familiar ve la bitácora en solo lectura

__APP__

1\.5

601, 602

AGE\-606

__App: documentos del expediente__

Subir, listar por categoría y ver documentos \(visor PDF/imagen\)\.

__✓ __Receta digitalizada del Sprint 4 aparece aquí

__APP\-R__

1

602

AGE\-607

__App: notas de relevo entre turnos__

Crear nota al cerrar turno y ver las últimas al iniciar; visible también para el familiar\.

__✓ __Última nota destacada en el check\-in del día

__APP\-R__

1

601

AGE\-608

__Web admin: moderación de contenido multimedia__

Cola de revisión de fotos/documentos reportados y política de retención de blobs eliminados\.

__✓ __Eliminar contenido lo retira de la app y lo audita

__WEB__

1\.5

602

AGE\-609

__Web admin: gestión del catálogo de productos \(marketplace\)__

CRUD de marketplace\_products con fotos, categorías, rango de precio y enlace externo\. API 14\.5–14\.6 se consumen desde la app en Sprint 9\.

__✓ __Producto publicado visible vía API pública

__✓ __Carga de hasta 5 fotos por producto

__WEB__

2\.5

602

AGE\-610

__Regresión de medio término__

Regresión completa de sprints 1–5 sobre build integrada, en matriz de dispositivos\. Gate de mitad de proyecto\.

__✓ __Cero bloqueantes y <5 mayores abiertos

__✓ __Informe de salud del proyecto al equipo

__QA__

2

—

AGE\-611

__Automatización: bitácora, documentos y WS de chat__

Pruebas API de bitácora/documentos y arnés de pruebas WebSocket \(conexión, orden de mensajes, reconexión\)\.

__✓ __Prueba de reconexión WS sin pérdida de mensajes

__QA__

2

603

## __Sprint 7 \(Semana 7\) — Chat en la app y asistente IA__

Objetivo: hub de Comunicación completo: chat humano con texto/voz/fotos en tiempo real y asistente IA sobre el expediente, incluido @asistente\.

__Demo: pregunta al asistente desde una tarjeta de Salud y conversación familiar\-cuidadora con nota de voz\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-701

__API asistente IA sobre el expediente__

Endpoints 10\.1–10\.3: construcción de contexto \(vitals, adherencia, observaciones, alertas\), llamada al LLM, persistencia de conversaciones, fuentes citadas y límites de uso\. Filtrado por permisos del rol\.

__✓ __Responde correctamente las 3 preguntas guía del documento de funcionalidades

__✓ __Nunca expone datos de otro paciente \(test adversarial\)

__✓ __Fuentes citadas apuntan a datos reales

__BE__

2\.5

601

AGE\-702

__@asistente dentro del chat humano__

Detección de mención en 11\.2, consulta al asistente y publicación de la respuesta como mensaje del canal\.

__✓ __Respuesta llega por WS como assistant\_reply

__BE__

0\.5

701, 603

AGE\-703

__API TTS y STT__

Endpoints 12\.6–12\.7 con Azure AI Speech y caché de audio por hash\.

__✓ __Texto repetido no re\-sintetiza \(cache hit\)

__✓ __STT de nota de voz clara ≥90% de precisión

__BE__

1

602

AGE\-704

__App: chat de coordinación__

UI de mensajes con burbujas, fotos, notas de voz, indicador de escritura, no leídos y tiempo real por WS con reconexión\. Separación de conversaciones por paciente\.

__✓ __Chat estable tras suspender/reanudar la app

__✓ __@asistente muestra la respuesta de la IA en el hilo

__APP__

2\.5

603, 702

AGE\-705

__App: pestaña Asistente IA \+ preguntar sobre esto__

Chat con el asistente, historial de conversaciones y punto de entrada contextual desde tarjetas de Salud \(context\_ref\)\.

__✓ __Desde una tarjeta de vitals se llega con la pregunta prellenada

__✓ __Fuentes mostradas como chips tocables

__APP__

1\.5

701

AGE\-706

__App: grabación y reproducción de notas de voz__

Componente de audio compartido \(chat y futuras reacciones\): grabar, previsualizar, subir por SAS, reproducir con progreso\.

__✓ __Audio funciona en iOS y Android con permisos correctos

__✓ __Límite 3 min con aviso

__APP\-R__

2

704

AGE\-707

__Web admin: auditoría del asistente IA__

Vista de conversaciones IA \(muestreo\), métricas de uso y botón de reporte de respuesta incorrecta para mejora del prompt\.

__✓ __Acceso restringido y auditado \(datos sensibles\)

__WEB__

1\.5

701

AGE\-708

__Web admin: CRUD de ofertas de trabajo__

Gestión de job\_offers para la vitrina premium de cuidadoras \(API 13\.9\)\.

__✓ __Oferta activa visible vía API con filtro por zona

__WEB__

1\.5

109

AGE\-709

__Web admin: métricas de comunicación__

Tarjetas de uso: mensajes/día, preguntas IA/día, latencia media del asistente\.

__✓ __Datos agregados sin exponer contenido de mensajes

__WEB__

1

707

AGE\-710

__Pruebas del asistente IA__

Set de 30 preguntas doradas con respuestas esperadas, pruebas de permisos \(cada rol\), inyección de prompt y comportamiento ante expediente vacío\.

__✓ __≥90% de las doradas correctas

__✓ __0 fugas de datos entre pacientes

__QA__

2

705

AGE\-711

__Pruebas de chat multi\-dispositivo__

Concurrencia con 4 participantes, redes lentas \(throttling\), reconexión, y push a desconectados\.

__✓ __Sin mensajes perdidos ni duplicados en 500 mensajes de prueba

__QA__

2

704

## __Sprint 8 \(Semana 8\) — Vista del adulto mayor y arranque del piloto__

Objetivo: experiencia del adulto mayor completa \(mosaicos accesibles, chat con voz, fotos, entretenimiento\) y salida del Release Candidate al grupo piloto\.

__HITO: inicio del piloto con usuarios reales \(TestFlight / Play interno\) al cierre del sprint\.__

*Carga del sprint: BE 4\.5d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-801

__API galería de fotos y reacciones__

Endpoints 12\.1–12\.4: publicar, listar, reaccionar \(corazón/voz\), eliminar\. Notificación amable a la familia por reacción\.

__✓ __Doble corazón responde ALREADY\_REACTED

__✓ __Reacción notifica sin crear alerta

__BE__

1\.5

602

AGE\-802

__API feed de entretenimiento__

Endpoint 12\.5 sirviendo content\_items curados desde la web admin con audio pregenerado\.

__✓ __Feed devuelve solo contenido activo del locale

__BE__

0\.5

509

AGE\-803

__API marketplace \(vitrina\)__

Endpoints 14\.1–14\.6: búsqueda de cuidadoras con filtros y destacados, perfil público, contacto, reseñas, catálogo de productos\.

__✓ __Destacadas \(premium\) aparecen primero

__✓ __Reseña duplicada responde ALREADY\_REVIEWED

__BE__

1\.5

201

AGE\-804

__Backend premium: validación de compras IAP__

Endpoints 13\.7–13\.8: verificación de recibos con Google Play y App Store, vigencia de suscripción y gating de funciones premium \(402\)\.

__✓ __Recibo sandbox activa premium

__✓ __Función premium sin plan responde PREMIUM\_REQUIRED

__BE__

1

107

AGE\-805

__App: vista del adulto mayor \(mosaicos accesibles\)__

Home con mosaicos grandes \(Familia, Fotos, Entretenimiento, Cómo me siento\), tipografía grande, alto contraste, sin barra inferior; detección de rol elder al entrar\.

__✓ __Objetivos táctiles ≥48dp y contraste AA verificados

__✓ __Check\-in con caritas alimenta la bitácora

__APP__

2

601

AGE\-806

__App: galería, slideshow y reacciones__

Galería para el adulto mayor con modo presentación y reacción corazón/nota de voz; publicación de fotos desde la vista del familiar\.

__✓ __Slideshow avanza solo con controles simples

__✓ __Familiar recibe la reacción en el chat/notificación

__APP__

1\.5

801

AGE\-807

__App: entretenimiento leer/escuchar__

Feed de chistes y noticias con controles grandes \(escuchar, pausar, siguiente\) usando audio pregenerado o TTS\.

__✓ __Modo escuchar funciona con pantalla bloqueada

__APP__

0\.5

802, 703

AGE\-808

__App: voz primero para el adulto mayor__

Dictado \(STT\) para escribir mensajes, lectura en voz alta de mensajes recibidos \(TTS\) y chat simplificado de la vista elder sobre el chat común\.

__✓ __Mensaje dictado→enviado sin tocar el teclado

__✓ __Mensaje recibido se lee en voz alta con un toque

__APP\-R__

2

703, 704

AGE\-809

__Web admin: moderación de reseñas y perfiles de cuidadoras__

Cola de aprobación de perfiles publicados al marketplace y moderación de reseñas reportadas\.

__✓ __Perfil no aprobado no aparece en búsqueda

__WEB__

2

803

AGE\-810

__Web admin: dashboard del piloto__

Métricas para seguir el piloto: activaciones, retención 7 días, alertas generadas/atendidas, crashes \(App Insights\), embudo de onboarding\.

__✓ __Datos del piloto visibles al día siguiente del arranque

__WEB__

2

209

AGE\-811

__Release Candidate del piloto: regresión completa__

Regresión total \(funcional \+ accesibilidad de la vista elder\), smoke en los 6 dispositivos y firma del RC\.

__✓ __Checklist de salida firmado; cero bloqueantes

__✓ __Accesibilidad elder validada con VoiceOver/TalkBack

__QA__

2\.5

805

AGE\-812

__Arranque del piloto__

Distribución a 15–25 usuarios piloto \(familias y cuidadoras\), guía de bienvenida, canal de feedback y formulario de reporte de problemas\.

__✓ __100% de pilotos con la app instalada y onboarding completado

__✓ __Canal de feedback con triage diario

__QA__

1\.5

811

## __Sprint 9 \(Semana 9\) — Marketplace en la app, premium y feedback del piloto__

Objetivo: cerrar el alcance funcional v1 \(marketplace, premium con IAP, reportes de cuidadora\) mientras se corrige el feedback temprano del piloto\.

__Demo: compra premium sandbox completa y marketplace navegable\. Congelación de alcance al cierre\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-901

__API reportes extendidos de la cuidadora__

Endpoint 13\.10: estadísticas por rango, serie diaria y exportación PDF \(plantilla con logo\)\. Límite 30 días para plan gratis\.

__✓ __PDF descargable con las métricas del rango

__✓ __Gratis limitado a 30 días con mensaje de upsell

__BE__

1\.5

804

AGE\-902

__Hardening de seguridad del backend__

Rate limiting, bitácora de acceso a datos clínicos, revisión de autorización endpoint por endpoint contra la matriz de permisos, escaneo de dependencias\.

__✓ __Checklist OWASP API Top 10 revisado y documentado

__✓ __Auditoría de acceso a expediente operativa

__BE__

1\.5

—

AGE\-903

__Correcciones backend del feedback piloto__

Bolsa de capacidad reservada para bugs y ajustes reportados por el piloto \(triage con QA\)\.

__✓ __Bloqueantes del piloto resueltos en <48 h

__BE__

1

812

AGE\-904

__App: marketplace \(cuidadoras y productos\)__

Búsqueda con filtros, perfil de cuidadora con reseñas, contactar, catálogo de productos con ficha y enlace externo, según wireframe Marketplace\.

__✓ __Filtros combinables con resultados <1 s

__✓ __Contactar muestra el canal preferido de la cuidadora

__APP__

2

803

AGE\-905

__App: premium con compra in\-app__

Paywall contextual en cada función premium \(foto al chat, ofertas, perfil destacado, reportes\), integración in\_app\_purchase, restauración de compras y pantalla Mi plan\.

__✓ __Compra sandbox en iOS y Android activa premium al instante

__✓ __Restaurar compras funciona tras reinstalar

__APP__

2

804

AGE\-906

__App: perfil profesional y ofertas \(cuidadora\)__

Edición del perfil profesional \(13\.5–13\.6\), listado de ofertas de trabajo premium y reportes con export\.

__✓ __Perfil publicado aparece en el marketplace

__✓ __Ofertas bloqueadas sin premium con paywall

__APP\-R__

1

905, 901

AGE\-907

__App: correcciones del feedback piloto__

Bolsa de capacidad para bugs de app reportados por pilotos\.

__✓ __Build corregida a pilotos antes del fin del sprint

__APP\-R__

1

812

AGE\-908

__Web admin: gestión de suscripciones__

Vista de suscripciones premium \(estado, tienda, vigencia\), otorgar premium cortesía y conciliación básica de recibos\.

__✓ __Cortesía auditada con motivo y vencimiento

__WEB__

1\.5

804

AGE\-909

__Web admin: mejoras operativas del piloto__

Ajustes al dashboard piloto según lo que el equipo necesite \(embudos, listas de usuarios activos, errores frecuentes\) y correcciones propias\.

__✓ __Reporte semanal del piloto generable en 1 clic

__WEB__

2\.5

810

AGE\-910

__Pruebas de compras IAP__

Matriz de compra: sandbox iOS/Android, cancelación, restauración, expiración, doble compra, y gating de cada función premium\.

__✓ __10 escenarios IAP ejecutados sin defectos críticos

__QA__

1\.5

905

AGE\-911

__Triage del piloto \+ regresión de comunicación__

Gestión diaria del feedback piloto \(reproducir, priorizar, verificar fixes\) y regresión de chat/IA/elder tras los cambios\.

__✓ __Backlog de piloto clasificado a diario

__✓ __Informe de retención y top\-5 problemas al cierre

__QA__

2\.5

812

## __Sprint 10 \(Semana 10\) — Estabilización y envío a tiendas__

Objetivo: congelación de código, calidad de release, materiales de tienda y envío a revisión de App Store y Google Play\.

__HITO: submission a ambas tiendas\. La publicación efectiva depende de la revisión \(3–7 días hábiles típicos; puede extenderse por ser app de salud\)\.__

*Carga del sprint: BE 4d · APP 4d · APP\-R 2d · WEB 4d · QA 4d*

__ID__

__Ticket y especificación__

__Rol__

__Días__

__Depende de__

AGE\-1001

__Rendimiento y robustez del backend__

Prueba de carga \(100 usuarios concurrentes, ingesta sostenida\), revisión de índices con EXPLAIN, tuning del pool de conexiones, alarmas de infraestructura \(App Insights\) y runbook de incidentes\.

__✓ __p95 <500 ms en endpoints de lectura bajo carga

__✓ __Alertas de infra configuradas \(errores 5xx, CPU, storage\)

__BE__

2

—

AGE\-1002

__Soporte de release y correcciones finales backend__

Congelación: solo fixes\. Migración y verificación del entorno productivo, rotación de secretos, backup verificado con restauración de prueba\.

__✓ __Restauración de backup probada en entorno aislado

__✓ __prod con datos limpios y seeds mínimos

__BE__

2

1001

AGE\-1003

__App: correcciones finales y pulido__

Cierre de bugs mayores del piloto, pulido visual contra wireframes, estados vacíos y de error, accesibilidad general\.

__✓ __Cero bloqueantes ni mayores abiertos

__✓ __Crash\-free rate ≥99\.5% en el piloto

__APP__

2

—

AGE\-1004

__Builds de release y fichas de tienda__

Builds firmadas de producción, fichas App Store/Play en español \(descripciones, keywords, capturas por dispositivo, video opcional\), clasificación de contenido y formularios de privacidad de datos \(App Privacy / Data Safety\) para datos de salud\.

__✓ __Formularios de privacidad coherentes con los datos reales que procesa la app

__✓ __Fichas completas en ambas consolas

__APP__

2

1003

AGE\-1005

__Gestión de revisión de tiendas__

Submission, cuenta demo para revisores \(con paciente demo y datos\), notas de revisión explicando el rol de salud/cuidado, y respuesta rápida a rechazos\.

__✓ __Enviado a ambas tiendas con cuenta demo funcional

__✓ __Plan de respuesta a rechazo en <24 h

__APP\-R__

2

1004

AGE\-1006

__Web admin: estabilización y manual de operación__

Cierre de bugs del panel, manual de operación \(curación de contenido, moderación, soporte, monitoreo de alertas\) para el equipo operativo\.

__✓ __Manual publicado y validado por una persona no técnica

__WEB__

2

—

AGE\-1007

__Páginas legales y de privacidad__

Páginas públicas requeridas por las tiendas: política de privacidad \(datos de salud, consentimiento\), términos de servicio y página de eliminación de cuenta \(requisito Google Play\)\.

__✓ __URLs públicas enlazadas en ambas fichas

__✓ __Flujo de eliminación de cuenta operativo end\-to\-end

__WEB__

2

—

AGE\-1008

__Regresión final y firma del release__

Regresión completa sobre la build candidata de producción, verificación en prod \(smoke\), y firma formal del release\.

__✓ __Acta de release firmada con resultados y riesgos conocidos

__QA__

2

1003

AGE\-1009

__Checklist de cumplimiento de tiendas__

Verificación contra guías de revisión: permisos justificados \(micrófono, cámara, notificaciones\), disclaimers de que la app no es dispositivo médico, edad mínima, IAP conforme a políticas\.

__✓ __Checklist Apple \+ Google completado sin pendientes

__✓ __Textos de permisos \(info\.plist / manifest\) revisados en español

__QA__

2

1004

# __6\. Gestión de riesgos__

__\#__

__Riesgo__

__Prob\.__

__Impacto__

__Mitigación__

R1

El alcance completo v1 no cabe en 10 semanas \(plan agresivo por decisión de negocio\)\.

Alta

Alto

Línea de corte 8\.3 revisada cada viernes en la review; recortar Could/Should sin tocar el núcleo de salud y alertas\.

R2

Revisión de tiendas rechaza la app \(datos de salud, permisos, IAP\)\.

Media

Alto

Checklist de cumplimiento \(AGE\-1009\) desde la semana 9, cuenta demo para revisores, formularios de privacidad exactos, respuesta a rechazo en <24 h\.

R3

Persona única de backend \(bus factor\): enfermedad o cuello de botella bloquea a los tres frentes\.

Media

Alto

Especificación de endpoints como contrato \+ mocks en app/web para no bloquearse; PRs revisados por WEB para conocimiento compartido\.

R4

Integración del wearable real indefinida\.

Alta

Medio

Simulador con interfaz desacoplada desde S3; decisión de dispositivo antes de S7 si se quiere en v1; si no, queda para fase 2 sin afectar el plan\.

R5

Push notifications con comportamiento distinto por fabricante Android \(Doze, batería\)\.

Media

Medio

Pruebas en dispositivos reales desde S4–S5 \(matriz QA\); recordatorios persistentes con doble vía \(push \+ alarma local\)\.

R6

Cuentas de desarrollador no listas a tiempo \(enrolamiento Apple\)\.

Media

Alto

Trámite en S1 \(AGE\-107\) como bloqueante señalado; verificación semanal\.

R7

Calidad de respuestas del asistente IA insuficiente o con fugas de datos\.

Media

Alto

Set de preguntas doradas \+ tests adversariales \(AGE\-710\); IA es Should: puede lanzarse detrás de un feature flag\.

R8

El piloto revela problemas de usabilidad profundos en la vista del adulto mayor\.

Media

Medio

Prueba de accesibilidad temprana en el RC \(AGE\-811\); la vista elder puede simplificarse a chat\+fotos si el entretenimiento falla\.

# __7\. Estrategia de calidad__

- Automatización API en CI desde el Sprint 1: cada endpoint entra al repositorio de pruebas en el mismo sprint en que se construye\.
- Pruebas E2E en dispositivos reales para lo crítico: alarmas de medicación, push de alertas, SOS y accesibilidad de la vista del adulto mayor\.
- Dos gates formales: regresión de medio término \(S6, AGE\-610\) y regresión de release \(S10, AGE\-1008\)\. Un gate no superado activa la línea de corte\.
- Piloto gestionado como fuente de verdad de calidad desde S8: triage diario, crash\-free ≥99\.5% como criterio de release\.

# __8\. Plan de release__

## __8\.1 Piloto \(semana 8\)__

15–25 usuarios en 2–3 círculos de cuidado reales \(familiar \+ cuidadora \+ adulto mayor\)\. Distribución por TestFlight y Play interno\. Objetivos: validar onboarding sin asistencia, utilidad del semáforo y las alertas, y usabilidad de la vista del adulto mayor\. Métricas en el dashboard del piloto \(AGE\-810\)\.

## __8\.2 Tiendas \(semana 10\)__

Submission simultáneo a App Store y Google Play al cierre del Sprint 10, con páginas legales públicas, formularios de privacidad de datos de salud, cuenta demo para revisores y notas de revisión\. La app se posiciona como herramienta de coordinación de cuidado, no como dispositivo médico ni app de diagnóstico — esto debe ser explícito en fichas y disclaimers para reducir el riesgo de rechazo\.

## __8\.3 Línea de corte \(si el plan se atrasa\)__

Orden de recorte acordado de antemano, del primero al último en salir:

- 1º Marketplace en la app \(EP\-12\): la vitrina puede lanzarse solo con el catálogo web o vacía con “próximamente”\. Ahorra ~4 días de APP en S9\.
- 2º Entretenimiento del adulto mayor \(parte de EP\-10\): chistes/noticias salen de v1; la vista elder queda con Familia \+ Fotos \+ check\-in\. Ahorra ~2 días\.
- 3º Reportes extendidos y ofertas de trabajo premium \(parte de EP\-11\): el paywall queda, las funciones dicen “próximamente”\. Ahorra ~3\.5 días\.
- 4º Asistente IA \(EP\-09\) detrás de feature flag: se lanza apagado y se activa por servidor cuando pase las pruebas doradas\. Ahorra ~6 días de riesgo\.
- Nunca se recortan: onboarding, vitals, medicamentos, alertas/SOS, chat básico, ni los requisitos de tiendas\.
