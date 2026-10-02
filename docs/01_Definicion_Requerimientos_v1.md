# AgeCare — Definición de Requerimientos

**Proyecto APT · Capstone PTY4614 · DUOC UC — Sede San Andrés**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Metodología:** Enfoque Tradicional (Cascada) · **Entrega:** 04 de octubre (avance Fase 2)

---

## 1. Propósito

Este documento consolida la **definición de requerimientos** del sistema AgeCare como avance
de la Fase 2 (Diseño del Sistema) del plan de trabajo en cascada. Toma como fuente única y
autoritativa el **Documento de Requerimientos (ERS simplificado)** entregado en Fase 1, del
cual conserva íntegramente la numeración **RF-01 … RF-82** y **RNF-01 … RNF-25**.

No redefine ni renumera requisitos: los **traza** hacia los objetivos específicos, hacia las
historias de usuario (entregable 02) y hacia el modelo de datos definitivo (entregable 03),
dejando explícito qué está soportado por el modelo construido a la fecha y qué corresponde a
etapas posteriores del cronograma.

---

## 2. Actores del sistema

| Actor | Rol en el cuidado |
|---|---|
| **Familiar** | Observa el estado del paciente, recibe alertas, consulta el expediente, administra el círculo de cuidado. Crea la cuenta y el paciente (administrador). |
| **Cuidadora** | Opera el día a día: confirma dosis, registra observaciones/incidentes/vitales manuales, activa emergencias. |
| **Médico** | Prescribe y ajusta el plan de medicamentos; revisa el expediente. Participación acotada. |
| **Adulto mayor** | Usuario activo con vista accesible de voz primero. No introduce credenciales (vinculación por código). |
| **Automático** | Procesos que ejecuta el propio sistema (generación de tomas, evaluación de alertas, escalamiento). |

---

## 3. Requisitos funcionales (RF-01 … RF-82)

Agrupados por módulo, según el ERS. La columna **Modelo** indica si el modelo de datos
definitivo (entregable 03) ya soporta físicamente el requisito: ✅ soportado · ⏳ etapa posterior.

### 3.1 Autenticación y cuentas

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-01 | Registrar cuenta con nombre, correo y contraseña. | Sin autenticar | ✅ |
| RF-02 | Iniciar sesión; devuelve pacientes asociados y rol en cada uno. | Sin autenticar | ✅ |
| RF-03 | Mantener la sesión activa renovándola automáticamente. | Todos | ✅ |
| RF-04 | Cerrar sesión y dejar de notificar a ese dispositivo. | Todos | ✅ |
| RF-05 | Recuperar contraseña por correo, cerrando todas las sesiones. | Sin autenticar | ✅ |
| RF-06 | Consultar y modificar el perfil (nombre, teléfono, foto, idioma). | Todos | ✅ |
| RF-07 | Registrar el dispositivo para notificaciones. | Todos | ✅ |

### 3.2 Pacientes y círculo de cuidado

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-08 | Crear el perfil del adulto mayor; el creador queda como administrador. | Familiar | ✅ |
| RF-09 | Consultar pacientes accesibles y el perfil completo de cada uno. | Todos | ✅ |
| RF-10 | Modificar los datos del paciente. | Familiar (admin.) | ✅ |
| RF-11 | Invitar al círculo con rol, mediante enlace de un solo uso con vencimiento. | Familiar (admin.) | ✅ |
| RF-12 | Aceptar invitación, con o sin cuenta previa. | Todos | ✅ |
| RF-13 | Consultar miembros del círculo e invitaciones pendientes. | Familiar, Médico | ✅ |
| RF-14 | Quitar a un miembro, sin poder eliminar al administrador. | Familiar (admin.) | ✅ |
| RF-15 | Vincular wearable (un solo dispositivo activo a la vez). | Familiar, Cuidadora | ✅ |
| RF-16 | Informar estado de sincronización del wearable (última medición, batería, inactividad). | Todos | ✅ |

### 3.3 Salud y signos vitales

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-17 | Recibir lotes de mediciones del wearable, descartando duplicadas. | Fam., Cuid., A. mayor | ✅ |
| RF-18 | Registrar mediciones manuales (presión, temperatura, glucosa). | Cuidadora | ✅ |
| RF-19 | Consultar historial por rango, agrupado por hora/día/semana. | Todos | ✅ |
| RF-20 | Entregar el último valor por tipo, indicando si está en rango. | Todos | ✅ |
| RF-21 | Consultar y configurar el rango normal de cada vital. | Familiar, Médico | ✅ |
| RF-22 | Calcular indicador diario de bienestar con sus motivos. | Todos | ✅ |
| RF-23 | Resumen del estado de todos los pacientes del usuario. | Todos | ✅ |

### 3.4 Medicamentos y adherencia

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-24 | Agregar medicamento (dosis, horarios, días, vigencia). | Cuidadora, Médico | ✅ |
| RF-25 | Consultar plan (vigentes y descontinuados). | Todos | ✅ |
| RF-26 | Modificar medicamento regenerando solo tomas futuras. | Cuidadora, Médico | ✅ |
| RF-27 | Descontinuar medicamento conservando historial. | Cuidadora, Médico | ✅ |
| RF-28 | Entregar tomas de una fecha con su estado y la próxima. | Todos | ✅ |
| RF-29 | Registrar toma administrada/pospuesta/omitida (motivo al omitir, límite al posponer). | Cuidadora | ✅ |
| RF-30 | Calcular adherencia por rango, por medicamento y por día. | Todos | ✅ |
| RF-31 | Fotografiar receta, extraer medicamentos (OCR) y proponerlos. | Cuidadora, Médico | ⏳ |
| RF-32 | Generar automáticamente las tomas del día siguiente (zona horaria del paciente). | Automático | ✅ |
| RF-33 | Marcar como omitida la toma vencida y notificar al familiar. | Automático | ✅ |

### 3.5 Bitácora del expediente

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-34 | Registrar observaciones por categoría, con foto opcional. | Cuidadora | ⏳ |
| RF-35 | Consultar la bitácora con filtros. | Todos | ⏳ |
| RF-36 | Registrar incidente (tipo, gravedad, hora); genera alerta si es crítico. | Cuidadora | ⏳ |
| RF-37 | Notas de relevo entre turnos. | Cuidadora, Familiar | ⏳ |
| RF-38 | Check-in diario del adulto mayor (uno por día). | Adulto mayor | ⏳ |

### 3.6 Archivos y documentos médicos

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-39 | Subir archivos por enlace temporal, validando tipo y tamaño. | Todos | ⏳ |
| RF-40 | Asociar archivo al expediente como documento médico. | Fam., Cuid., Médico | ⏳ |
| RF-41 | Consultar documentos con filtro por categoría. | Todos | ⏳ |
| RF-42 | Descargar/visualizar documento por enlace temporal corto. | Todos | ⏳ |
| RF-43 | Eliminar documento conservando registro, con depuración posterior. | Familiar (admin.), autor | ⏳ |

### 3.7 Alertas y emergencias

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-44 | Generar alertas por caída, vital fuera de rango, toma no administrada y wearable sin datos. | Automático | ✅ |
| RF-45 | Notificar al teléfono respetando preferencias. | Automático | ✅ |
| RF-46 | Evitar alertas repetidas por la misma condición en un intervalo. | Automático | ✅ |
| RF-47 | Listar alertas de todos los pacientes, con filtro y no leídas. | Todos | ✅ |
| RF-48 | Marcar alerta como atendida, deteniendo recordatorios. | Familiar, Cuidadora | ✅ |
| RF-49 | Cerrar alerta con nota de resolución, conservándola. | Familiar, Cuidadora | ✅ |
| RF-50 | Consultar/modificar preferencias por tipo; caída y emergencia no desactivables. | Todos | ✅ |
| RF-51 | Activar emergencia (botón): alerta crítica, aviso a familiares, registro y teléfonos de contacto. | Cuidadora, A. mayor | ✅ |
| RF-52 | Escalar la alerta a los siguientes contactos si nadie la atiende a tiempo. | Automático | ✅ |

### 3.8 Comunicación

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-53 | Canal de conversación por paciente (texto, voz, foto). | Todos | ⏳ |
| RF-54 | Entregar mensajes en tiempo real y por notificación a desconectados. | Todos | ⏳ |
| RF-55 | Consultar historial y controlar no leídos. | Todos | ⏳ |
| RF-56 | Consultar al asistente IA sobre el expediente, citando fuentes. | Todos | ⏳ |
| RF-57 | Restringir respuestas del asistente a lo permitido por el rol. | Automático | ⏳ |
| RF-58 | Invocar al asistente dentro del chat humano. | Todos | ⏳ |
| RF-59 | Conservar el historial de conversaciones con el asistente. | Todos | ⏳ |

### 3.9 Vista del adulto mayor

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-60 | Publicar fotografías en galería visible para el adulto mayor. | Familiar | ⏳ |
| RF-61 | Ver galería en presentación y reaccionar (gesto o nota de voz). | Adulto mayor | ⏳ |
| RF-62 | Entregar contenido de entretenimiento (leer o escuchar). | A. mayor, Familiar | ⏳ |
| RF-63 | Leer en voz alta mensajes y contenidos. | Todos | ⏳ |
| RF-64 | Escribir mensajes por dictado de voz. | Todos | ⏳ |
| RF-65 | Crear música por gestos frente a la cámara (audio en el dispositivo). | Adulto mayor | ⏳ |
| RF-66 | Conservar creaciones y sincronizarlas sin duplicar. | Automático | ⏳ |
| RF-67 | Compartir creaciones por enlace seguro de escucha. | A. mayor, Familiar | ⏳ |
| RF-68 | Vincular dispositivo del adulto mayor por código, sin credenciales. | Cuidadora, Familiar | ⏳ |
| RF-69 | Registrar métricas de uso por sesión de actividad. | Automático | ⏳ |

> **Nota de alcance (módulo Director Musical, RF-65 a RF-69):** forma parte de la vista del
> adulto mayor y depende de servicios de Alloxentric (incluida la configuración de Azure
> correspondiente). Se documenta como parte del alcance total, pero su implementación es
> posterior al núcleo de salud.

### 3.10 Operación diaria de la cuidadora

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-70 | Vista del día: paciente, próxima toma, tareas, alertas y última nota de relevo. | Cuidadora | ⏳ |
| RF-71 | Crear, consultar y marcar tareas de cuidado por categoría. | Cuidadora, Familiar | ⏳ |
| RF-72 | Mantener perfil profesional (experiencia, especialidades, idiomas, zonas, certificaciones). | Cuidadora | ⏳ |
| RF-73 | Distinguir funciones gratuitas de pago; bloquear premium sin suscripción. | Automático | ⏳ |
| RF-74 | Generar reportes de actividad por rango de fechas. | Cuidadora | ⏳ |

### 3.11 Marketplace

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-75 | Buscar cuidadoras con filtros (zona, especialidad, idioma, calificación). | Familiar | ⏳ |
| RF-76 | Consultar perfil público de una cuidadora y sus reseñas. | Familiar | ⏳ |
| RF-77 | Registrar solicitud de contacto y entregar canal. | Familiar | ⏳ |
| RF-78 | Dejar reseña solo quien tuvo a la cuidadora en su círculo, una vez. | Familiar | ⏳ |
| RF-79 | Consultar catálogo de artículos de apoyo por categoría. | Familiar, Cuidadora | ⏳ |

### 3.12 Funcionamiento sin conexión

| RF | Requisito | Roles | Modelo |
|---|---|---|---|
| RF-80 | Conservar localmente la información para operar sin conexión. | Todos | ⏳ |
| RF-81 | Sincronizar al recuperar señal, sin duplicar ni perder. | Automático | ⏳ |
| RF-82 | Vía alternativa de aviso cuando la notificación no se pueda entregar. | Automático | ⏳ |

---

## 4. Requisitos no funcionales (RNF-01 … RNF-25)

| RNF | Categoría | Criterio | Soporte |
|---|---|---|---|
| RNF-01 | Rendimiento | Lote de 500 mediciones < 1 s. | ✅ |
| RNF-02 | Rendimiento | Serie de 30 días agrupada por día < 300 ms. | ✅ |
| RNF-03 | Rendimiento | 95% de lecturas < 500 ms bajo carga. | ✅ (índices + particionado) |
| RNF-04 | Rendimiento | Caída → alerta y aviso < 10 s. | ✅ |
| RNF-05 | Rendimiento | Notificación entregada < 30 s. | ✅ (`alert_deliveries`) |
| RNF-06 | Escalabilidad | ≥ 100 usuarios concurrentes sin degradar. | ✅ (infra) |
| RNF-07 | Escalabilidad | Mediciones particionadas por mes. | ✅ (`vital_readings`) |
| RNF-08 | Escalabilidad | Ingesta repetible sin duplicar. | ✅ (UNIQUE natural) |
| RNF-09 | Seguridad | TLS 1.2+ en tránsito. | ✅ (infra) |
| RNF-10 | Seguridad | Contraseñas con hash, nunca texto plano. | ✅ (`users.password_hash`) |
| RNF-11 | Seguridad | Sesión 30 min + refresh rotatorio revocable 30 días. | ✅ (`refresh_tokens`) |
| RNF-12 | Seguridad | Control de acceso en servidor por rol sobre el paciente. | ✅ (`patient_members`) |
| RNF-13 | Seguridad | Enlaces de archivos expiran ≤ 15 min. | ⏳ (SAS, etapa archivos) |
| RNF-14 | Seguridad | Trazabilidad: quién consultó qué expediente y cuándo. | ⏳ (auditoría) |
| RNF-15 | Seguridad | Cifrado en reposo de BD y archivos. | ✅ (infra Azure) |
| RNF-16 | Disponibilidad | Operación sin conexión con sincronización. | ⏳ (offline) |
| RNF-17 | Disponibilidad | Respaldos automáticos + restauración verificada. | ✅ (infra) |
| RNF-18 | Disponibilidad | Sesiones sin fallos ≥ 99,5%. | ⏳ (app) |
| RNF-19 | Usabilidad | Táctiles ≥ 48 pt y contraste AA en vista del adulto mayor. | ⏳ (app) |
| RNF-20 | Usabilidad | Acciones principales del adulto mayor sin teclado. | ⏳ (app) |
| RNF-21 | Usabilidad | Interfaz y errores en español. | ✅ |
| RNF-22 | Portabilidad | Servidor y BD en Docker, un solo archivo de composición. | ✅ (`docker-compose.yml`) |
| RNF-23 | Portabilidad | Configuración por variables de entorno. | ✅ (`.env`) |
| RNF-24 | Mantenibilidad | Cambios de BD por migraciones versionadas y reversibles. | ✅ |
| RNF-25 | Mantenibilidad | Documentación de servicios generada desde el código. | ✅ (OpenAPI `/docs`) |

---

## 5. Trazabilidad objetivos ↔ requisitos

| Objetivo específico (ERS §3.2) | Requisitos | Estado del modelo |
|---|---|---|
| OE-1 Expediente único + semáforo | RF-08…23, RF-34…43 | ✅ núcleo / ⏳ bitácora y archivos |
| OE-2 Alertas en tiempo real + emergencia | RF-33, RF-44…52 | ✅ |
| OE-3 Ciclo de medicación | RF-24…33 | ✅ (OCR ⏳) |
| OE-4 Comunicación + asistente IA | RF-53…59 | ⏳ |
| OE-5 Experiencia del adulto mayor | RF-38, RF-60…69 | ⏳ |

---

## 6. Nota de transparencia sobre el alcance (Cascada)

El modelo de datos definitivo (entregable 03) implementa el **núcleo de salud**: autenticación,
pacientes y círculo de cuidado, signos vitales, medicamentos y adherencia, y alertas/emergencias
(RF-01 a RF-33 y RF-44 a RF-52). Esto corresponde al avance comprometido para el **04 de octubre**
dentro de la Fase 2 del cronograma.

Los módulos de bitácora, archivos, comunicación, asistente IA, vista del adulto mayor
(incluido Director Musical), operación profesional de la cuidadora, marketplace y
funcionamiento sin conexión están **especificados en el ERS** y **declarados aquí**; su
construcción se completa en el resto de la Fase 2 según la Carta Gantt. El diseño del núcleo
los admite por extensión, sin rediseño de las tablas existentes.
