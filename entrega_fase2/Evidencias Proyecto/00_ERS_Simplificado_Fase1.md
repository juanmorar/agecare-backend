**AgeCare**

Plataforma de cuidado de adultos mayores

Documento ERS

Capstone · PTY4614 · Portafolio de Título

Jazna Patricia Meza Hidalgo \| Juan Pablo Mellado Alarcon

Javier Cerna · Juan Mora · Benja Camus

**Índice**

1. Introducción

> 1.1 Propósito del documento
>
> 1.2 Alcance

2. Problema

3. Objetivos

> 3.1 Objetivo general
>
> 3.2 Objetivos específicos

4. Requisitos funcionales

> 4.1 Autenticación y cuentas
>
> 4.2 Pacientes y círculo de cuidado
>
> 4.3 Salud y signos vitales
>
> 4.4 Medicamentos y adherencia
>
> 4.5 Bitácora del expediente
>
> 4.6 Archivos y documentos médicos
>
> 4.7 Alertas y emergencias
>
> 4.8 Comunicación
>
> 4.9 Vista del adulto mayor
>
> 4.10 Operación diaria de la cuidadora
>
> 4.11 Marketplace
>
> 4.12 Funcionamiento sin conexión

5. Requisitos no funcionales

> 5.1 Rendimiento
>
> 5.2 Escalabilidad
>
> 5.3 Seguridad
>
> 5.4 Disponibilidad
>
> 5.5 Usabilidad y accesibilidad
>
> 5.6 Portabilidad y despliegue
>
> 5.7 Mantenibilidad

6. Casos de uso

> CU-01 --- Configurar el círculo de cuidado
>
> CU-02 --- Registrar mediciones y detectar una anomalía
>
> CU-03 --- Administrar una toma de medicamento
>
> CU-04 --- Digitalizar una receta médica
>
> CU-05 --- Atender una emergencia
>
> CU-06 --- Consultar el estado del paciente al asistente
>
> CU-07 --- Comunicarse desde la vista del adulto mayor

# **1. Introducción**

## **1.1 Propósito del documento**

Este documento especifica los requerimientos del sistema AgeCare: el problema que resuelve, los objetivos que persigue, lo que el sistema debe hacer y las condiciones de calidad que debe cumplir. Está dirigido al equipo de desarrollo, al docente de la asignatura y a la contraparte de la empresa.

Sirve como referencia única del proyecto: toda decisión sobre lo que se construye debe poder rastrearse hasta lo que aquí está escrito.

## **1.2 Alcance**

AgeCare es una plataforma de cuidado de adultos mayores con cuatro perfiles de usuario: el familiar, la cuidadora, el médico y el adulto mayor. El sistema reúne en un solo lugar la información de salud de la persona, genera alertas ante situaciones críticas y permite la comunicación entre quienes participan de su cuidado.

El alcance de este documento cubre el seguimiento de salud a partir del wearable y de los registros de la cuidadora, la gestión de medicamentos y su adherencia, el sistema de alertas y emergencias, la comunicación entre los miembros del círculo de cuidado, y la vista propia del adulto mayor.

# **2. Problema**

El cuidado de un adulto mayor dependiente recae casi siempre sobre su familia, y hoy se sostiene con herramientas que no fueron pensadas para eso. El reloj inteligente muestra sus datos en una aplicación aparte, la coordinación con la cuidadora ocurre por mensajería instantánea, las recetas médicas quedan como fotografías en el teléfono y lo que ocurre durante el día simplemente no se registra en ninguna parte.

Cuando un familiar que vive lejos quiere saber cómo está su madre o su padre, no tiene una respuesta clara. Tiene pedazos de información que debe juntar a mano.

Esa dispersión tiene consecuencias concretas. Una dosis que no se administró pasa desapercibida hasta que aparece algún efecto. Una caída se avisa por llamada telefónica, si es que hay alguien cerca. El médico prescribe sin saber si el tratamiento se está cumpliendo. Y el adulto mayor, que es el centro de todo esto, queda como objeto de monitoreo y no como participante.

En Chile el problema es amplio. Casi 4 millones de personas tienen 60 años o más, y cerca de cuatro de cada diez necesitan ayuda de otra persona para su vida diaria. Esa ayuda la entregan mayoritariamente las familias, sin herramientas ni apoyo formal.

El problema de fondo no es la falta de dispositivos, sino que la información existe repartida y nunca se integra en un lugar único, confiable y compartido por quienes cuidan.

# **3. Objetivos**

## **3.1 Objetivo general**

Desarrollar una plataforma digital integral de cuidado de adultos mayores que centralice el monitoreo de salud, las alertas, la coordinación del cuidado y la comunicación entre familiares, cuidadores, médicos y el propio adulto mayor, con el fin de proporcionar a las familias que cuidan a distancia información confiable y en tiempo real sobre el bienestar de su ser querido, y al adulto mayor un medio accesible para mantenerse conectado, acompañado y activo.

## **3.2 Objetivos específicos**

1.  Consolidar en un expediente único y compartido la información de salud del adulto mayor ---signos vitales del wearable, adherencia a medicamentos, observaciones de la cuidadora, incidentes y documentos médicos---, presentada mediante un semáforo de bienestar diario y con soporte multi-paciente.

2.  Implementar un sistema de alertas en tiempo real, con notificaciones al teléfono y umbrales configurables, que detecte y comunique los eventos críticos del cuidado: caída detectada, signo vital fuera de rango y medicamento no administrado, incluyendo un flujo de acción inmediata ante caídas y un botón de emergencia.

3.  Gestionar el ciclo completo de la medicación: definición del plan por la cuidadora o el médico, digitalización de recetas mediante reconocimiento de texto, alarmas de tomas, confirmación de dosis y visualización de la adherencia por parte del familiar.

4.  Facilitar la comunicación y la coordinación del círculo de cuidado mediante un chat contextual al paciente, con texto, voz y fotografías, y un asistente de inteligencia artificial capaz de interpretar el expediente y responder preguntas en lenguaje natural.

5.  Ofrecer al adulto mayor una experiencia propia, accesible y de voz primero, que lo integre como usuario activo de la plataforma: comunicación con su familia, fotografías compartidas, entretenimiento y creación musical mediante el módulo Director Musical.

# **4. Requisitos funcionales**

Los requisitos se agrupan por módulo funcional. La columna «Roles» indica quién puede ejecutar cada acción. «Sin autenticar» significa que no se requiere haber iniciado sesión; «Todos los roles» se refiere a familiar, cuidadora, médico y adulto mayor con sesión activa; «Automático» corresponde a procesos que ejecuta el propio sistema sin intervención del usuario.

## **4.1 Autenticación y cuentas**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-01 | El sistema debe permitir a un usuario registrar una cuenta con nombre, correo y contraseña. | Sin autenticar |
| RF-02 | El sistema debe permitir iniciar sesión con correo y contraseña, devolviendo los pacientes asociados y el rol del usuario en cada uno. | Sin autenticar |
| RF-03 | El sistema debe mantener la sesión activa renovándola automáticamente, sin obligar al usuario a iniciar sesión de nuevo. | Todos los roles |
| RF-04 | El sistema debe permitir cerrar sesión y dejar de enviar notificaciones a ese dispositivo. | Todos los roles |
| RF-05 | El sistema debe permitir recuperar la contraseña mediante un correo electrónico y establecer una nueva, cerrando todas las sesiones abiertas. | Sin autenticar |
| RF-06 | El sistema debe permitir a cada usuario consultar y modificar su perfil: nombre, teléfono, foto e idioma. | Todos los roles |
| RF-07 | El sistema debe registrar el dispositivo del usuario para poder enviarle notificaciones. | Todos los roles |

## **4.2 Pacientes y círculo de cuidado**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-08 | El sistema debe permitir al familiar crear el perfil de un adulto mayor, quedando como administrador de ese paciente. | Familiar |
| RF-09 | El sistema debe permitir consultar los pacientes a los que el usuario tiene acceso y el perfil completo de cada uno. | Todos los roles |
| RF-10 | El sistema debe permitir al administrador modificar los datos del paciente. | Familiar (admin.) |
| RF-11 | El sistema debe permitir invitar a una persona al círculo de cuidado asignándole un rol, mediante un enlace de un solo uso con vencimiento. | Familiar (admin.) |
| RF-12 | El sistema debe permitir aceptar una invitación, con o sin cuenta previa. | Todos los roles |
| RF-13 | El sistema debe permitir consultar quiénes forman el círculo de cuidado y qué invitaciones están pendientes. | Familiar, Médico |
| RF-14 | El sistema debe permitir quitar a un miembro del círculo de cuidado, sin poder eliminar al administrador. | Familiar (admin.) |
| RF-15 | El sistema debe permitir vincular un wearable al paciente, admitiendo un solo dispositivo activo a la vez. | Familiar, Cuidadora |
| RF-16 | El sistema debe informar el estado de sincronización del wearable: última medición, batería y si lleva demasiado tiempo sin enviar datos. | Todos los roles |

## **4.3 Salud y signos vitales**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-17 | El sistema debe recibir lotes de mediciones enviadas desde el wearable, descartando las ya registradas. | Familiar, Cuidadora, Adulto mayor |
| RF-18 | El sistema debe permitir registrar mediciones tomadas manualmente, como presión arterial, temperatura o glucosa. | Cuidadora |
| RF-19 | El sistema debe permitir consultar el historial de un signo vital en un rango de fechas, agrupado por hora, día o semana. | Todos los roles |
| RF-20 | El sistema debe entregar el último valor de cada signo vital, indicando si está dentro del rango normal. | Todos los roles |
| RF-21 | El sistema debe permitir consultar y configurar el rango normal de cada signo vital, validando que el mínimo no supere al máximo. | Familiar, Médico |
| RF-22 | El sistema debe calcular un indicador diario de bienestar a partir de las mediciones, la adherencia y los eventos del día, señalando los motivos del resultado. | Todos los roles |
| RF-23 | El sistema debe entregar un resumen del estado de todos los pacientes del usuario, para quienes tienen más de uno a cargo. | Todos los roles |

## **4.4 Medicamentos y adherencia**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-24 | El sistema debe permitir agregar un medicamento al plan, indicando dosis, horarios, días de la semana y vigencia. | Cuidadora, Médico |
| RF-25 | El sistema debe permitir consultar el plan de medicamentos, vigentes y descontinuados. | Todos los roles |
| RF-26 | El sistema debe permitir modificar un medicamento, regenerando solo las tomas futuras y conservando el historial. | Cuidadora, Médico |
| RF-27 | El sistema debe permitir descontinuar un medicamento, cancelando sus tomas futuras y conservando el registro de las administradas. | Cuidadora, Médico |
| RF-28 | El sistema debe entregar las tomas programadas de una fecha con su estado, señalando cuál es la próxima. | Todos los roles |
| RF-29 | El sistema debe permitir registrar una toma como administrada, pospuesta u omitida, exigiendo motivo al omitir y limitando la postergación. | Cuidadora |
| RF-30 | El sistema debe calcular el porcentaje de adherencia en un rango de fechas, desglosado por medicamento y por día. | Todos los roles |
| RF-31 | El sistema debe permitir fotografiar una receta, extraer automáticamente los medicamentos indicados y proponerlos para revisión antes de agregarlos al plan. | Cuidadora, Médico |
| RF-32 | El sistema debe generar automáticamente las tomas del día siguiente según la zona horaria del paciente. | Automático |
| RF-33 | El sistema debe marcar como omitida toda toma no confirmada dentro de su plazo y notificarlo al familiar. | Automático |

## **4.5 Bitácora del expediente**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-34 | El sistema debe permitir registrar observaciones del día clasificadas por categoría, con la opción de adjuntar una fotografía. | Cuidadora |
| RF-35 | El sistema debe permitir consultar la bitácora, con filtros por categoría, autor y rango de fechas. | Todos los roles |
| RF-36 | El sistema debe permitir registrar un incidente con tipo, gravedad, hora y descripción, generando una alerta cuando la gravedad sea crítica. | Cuidadora |
| RF-37 | El sistema debe permitir dejar y consultar notas de relevo entre turnos. | Cuidadora, Familiar |
| RF-38 | El sistema debe permitir al adulto mayor registrar cómo se siente, admitiendo un registro por día que reemplaza al anterior. | Adulto mayor |

## **4.6 Archivos y documentos médicos**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-39 | El sistema debe permitir subir archivos mediante un enlace temporal, validando tipo y tamaño según su uso. | Todos los roles |
| RF-40 | El sistema debe permitir asociar un archivo subido al expediente como documento médico, con título, categoría y fecha. | Familiar, Cuidadora, Médico |
| RF-41 | El sistema debe permitir consultar los documentos del expediente con filtro por categoría. | Todos los roles |
| RF-42 | El sistema debe permitir descargar o visualizar un documento mediante un enlace temporal de corta duración. | Todos los roles |
| RF-43 | El sistema debe permitir eliminar un documento conservando el registro, y depurar el archivo posteriormente. | Familiar (admin.), autor |

## **4.7 Alertas y emergencias**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-44 | El sistema debe generar alertas automáticamente ante una caída detectada, un signo vital fuera de rango, una toma no administrada o la falta prolongada de datos del wearable. | Automático |
| RF-45 | El sistema debe enviar una notificación al teléfono de los usuarios correspondientes al generarse una alerta, respetando las preferencias de cada uno. | Automático |
| RF-46 | El sistema debe evitar generar alertas repetidas por la misma condición dentro de un intervalo definido. | Automático |
| RF-47 | El sistema debe entregar el listado de alertas de todos los pacientes del usuario, con filtro por estado y el número de alertas sin leer. | Todos los roles |
| RF-48 | El sistema debe permitir marcar una alerta como atendida, deteniendo los recordatorios asociados. | Familiar, Cuidadora |
| RF-49 | El sistema debe permitir cerrar una alerta con una nota de resolución, conservándola en el historial. | Familiar, Cuidadora |
| RF-50 | El sistema debe permitir consultar y modificar las preferencias de notificación por tipo de alerta, impidiendo desactivar las de caída y emergencia. | Todos los roles |
| RF-51 | El sistema debe permitir activar una emergencia mediante un botón, generando una alerta crítica, notificando de inmediato a todos los familiares, registrando el evento y entregando los teléfonos de contacto. | Cuidadora, Adulto mayor |
| RF-52 | El sistema debe escalar la alerta a los siguientes contactos definidos cuando nadie la atienda dentro del plazo establecido. | Automático |

## **4.8 Comunicación**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-53 | El sistema debe proveer un canal de conversación por paciente que admita mensajes de texto, notas de voz y fotografías. | Todos los roles |
| RF-54 | El sistema debe entregar los mensajes en tiempo real a los participantes conectados y por notificación a quienes no lo estén. | Todos los roles |
| RF-55 | El sistema debe permitir consultar el historial de la conversación y llevar el control de los mensajes no leídos. | Todos los roles |
| RF-56 | El sistema debe permitir consultar al asistente de inteligencia artificial sobre el expediente del paciente, indicando los datos en que se basa la respuesta. | Todos los roles |
| RF-57 | El sistema debe restringir las respuestas del asistente a la información que el rol del usuario tiene permitido ver. | Automático |
| RF-58 | El sistema debe permitir invocar al asistente dentro de la conversación entre personas y publicar su respuesta como un mensaje más del canal. | Todos los roles |
| RF-59 | El sistema debe conservar el historial de conversaciones con el asistente. | Todos los roles |

## **4.9 Vista del adulto mayor**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-60 | El sistema debe permitir a los familiares publicar fotografías en una galería visible para el adulto mayor. | Familiar |
| RF-61 | El sistema debe permitir al adulto mayor ver la galería en modo presentación y reaccionar a una fotografía con un gesto simple o una nota de voz. | Adulto mayor |
| RF-62 | El sistema debe entregar contenido de entretenimiento seleccionado, disponible para leer o escuchar. | Adulto mayor, Familiar |
| RF-63 | El sistema debe permitir escuchar en voz alta los mensajes y contenidos recibidos. | Todos los roles |
| RF-64 | El sistema debe permitir escribir mensajes mediante dictado por voz. | Todos los roles |
| RF-65 | El sistema debe permitir al adulto mayor crear música mediante gestos de las manos frente a la cámara, generando el audio en el propio dispositivo. | Adulto mayor |
| RF-66 | El sistema debe conservar las creaciones musicales y sincronizarlas con el servidor al recuperar la conexión, sin duplicarlas. | Automático |
| RF-67 | El sistema debe permitir compartir las creaciones musicales con la familia mediante un enlace seguro de escucha. | Adulto mayor, Familiar |
| RF-68 | El sistema debe permitir vincular el dispositivo del adulto mayor mediante un código simple, sin que deba introducir credenciales. | Cuidadora, Familiar |
| RF-69 | El sistema debe registrar métricas de uso por sesión de actividad del adulto mayor, para seguimiento de sus cuidadores. | Automático |

## **4.10 Operación diaria de la cuidadora**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-70 | El sistema debe entregar a la cuidadora una vista con el estado del día: paciente a cargo, próxima toma, tareas pendientes, alertas activas y última nota de relevo. | Cuidadora |
| RF-71 | El sistema debe permitir crear, consultar y marcar las tareas de cuidado del día por categoría. | Cuidadora, Familiar |
| RF-72 | El sistema debe permitir a la cuidadora mantener su perfil profesional con experiencia, especialidades, idiomas, zonas y certificaciones. | Cuidadora |
| RF-73 | El sistema debe distinguir entre funciones gratuitas y funciones de pago, impidiendo el acceso a estas últimas sin una suscripción vigente. | Automático |
| RF-74 | El sistema debe permitir generar reportes de la actividad realizada en un rango de fechas. | Cuidadora |

## **4.11 Marketplace**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-75 | El sistema debe permitir buscar cuidadoras aplicando filtros por zona, especialidad, idioma y calificación. | Familiar |
| RF-76 | El sistema debe permitir consultar el perfil público de una cuidadora junto con sus reseñas. | Familiar |
| RF-77 | El sistema debe registrar la solicitud de contacto hacia una cuidadora y entregar su canal de contacto. | Familiar |
| RF-78 | El sistema debe permitir dejar una reseña únicamente a quien haya tenido a la cuidadora en su círculo de cuidado, y solo una vez. | Familiar |
| RF-79 | El sistema debe permitir consultar el catálogo de artículos de apoyo por categoría. | Familiar, Cuidadora |

## **4.12 Funcionamiento sin conexión**

| **Código** | **Requisito** | **Roles** |
|:---|----|----|
| RF-80 | La aplicación debe conservar localmente la información necesaria para seguir operando cuando el dispositivo no tenga conexión. | Todos los roles |
| RF-81 | La aplicación debe sincronizar con el servidor los registros generados sin conexión al restablecerse la señal, sin duplicarlos ni perderlos. | Automático |
| RF-82 | El sistema debe ofrecer una vía alternativa de aviso cuando la notificación al teléfono no pueda entregarse. | Automático |

# **5. Requisitos no funcionales**

Los requisitos no funcionales definen las condiciones de calidad que el sistema debe cumplir. Cada uno se expresa con un criterio verificable.

## **5.1 Rendimiento**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-01 | Procesamiento de mediciones del wearable | Un lote de hasta 500 mediciones debe procesarse en menos de 1 segundo. |
| RNF-02 | Consulta de historial | Una serie de 30 días agrupada por día debe responder en menos de 300 milisegundos. |
| RNF-03 | Tiempo de respuesta general | El 95 % de las consultas de lectura debe responder en menos de 500 milisegundos bajo carga. |
| RNF-04 | Latencia de alertas críticas | Una caída detectada debe generar la alerta y el aviso al teléfono en menos de 10 segundos. |
| RNF-05 | Entrega de notificaciones | Una notificación debe llegar al dispositivo en menos de 30 segundos. |

## **5.2 Escalabilidad**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-06 | Usuarios concurrentes | El sistema debe sostener al menos 100 usuarios simultáneos sin degradar los tiempos anteriores. |
| RNF-07 | Crecimiento de las mediciones | La tabla de mediciones debe estar particionada por mes para mantener el rendimiento de las consultas históricas. |
| RNF-08 | Ingesta repetible | El envío duplicado de un mismo lote no debe generar registros repetidos ni alertas repetidas. |

## **5.3 Seguridad**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-09 | Cifrado en tránsito | Toda comunicación con el servidor debe usar TLS 1.2 o superior. |
| RNF-10 | Resguardo de contraseñas | Las contraseñas deben almacenarse con función de hash, nunca en texto plano. |
| RNF-11 | Duración de la sesión | La sesión debe expirar a los 30 minutos y renovarse mediante un mecanismo rotatorio revocable de 30 días. |
| RNF-12 | Control de acceso | Cada operación debe validar en el servidor el rol del usuario sobre el paciente; ocultar la opción en la interfaz no se considera control de acceso. |
| RNF-13 | Acceso a archivos | Los enlaces de subida y descarga de archivos deben expirar en un máximo de 15 minutos. |
| RNF-14 | Trazabilidad clínica | El sistema debe registrar qué usuario consultó qué expediente y cuándo. |
| RNF-15 | Cifrado en reposo | La base de datos y los archivos almacenados deben estar cifrados en reposo. |

## **5.4 Disponibilidad**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-16 | Operación sin conexión | La aplicación debe permitir consultar y registrar información básica sin conexión, sincronizando al recuperarla. |
| RNF-17 | Respaldos | La base de datos debe contar con respaldos automáticos y con un procedimiento de restauración verificado. |
| RNF-18 | Estabilidad de la aplicación | La aplicación debe mantener una tasa de sesiones sin fallos igual o superior al 99,5 %. |

## **5.5 Usabilidad y accesibilidad**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-19 | Accesibilidad del adulto mayor | En la vista del adulto mayor los elementos táctiles deben medir al menos 48 puntos y el contraste debe cumplir el nivel AA. |
| RNF-20 | Interacción por voz | La vista del adulto mayor debe permitir completar sus acciones principales sin usar el teclado. |
| RNF-21 | Idioma | La interfaz y los mensajes de error deben estar en español. |

## **5.6 Portabilidad y despliegue**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-22 | Contenedores | El servidor y la base de datos deben ejecutarse en contenedores Docker y levantarse mediante un único archivo de composición. |
| RNF-23 | Configuración externa | Las credenciales y parámetros del entorno deben definirse mediante variables de entorno, sin quedar escritos en el código. |

## **5.7 Mantenibilidad**

| **Código** | **Requisito** | **Criterio de cumplimiento** |
|:---|----|----|
| RNF-24 | Control de cambios en la base de datos | Todo cambio de estructura debe aplicarse mediante migraciones versionadas y reversibles. |
| RNF-25 | Documentación de la interfaz | La documentación de los servicios debe generarse automáticamente a partir del código. |

# **6. Casos de uso**

Se describen los casos de uso principales del sistema. Cada uno indica el actor que lo inicia, las condiciones previas, el flujo principal, el resultado esperado y los requisitos funcionales que cubre.

## **CU-01 --- Configurar el círculo de cuidado**

**Actor:** Familiar (administrador)

**Precondición:** El familiar tiene una cuenta creada.

**Flujo principal:**

> 1\. El familiar crea el perfil del adulto mayor con sus datos y padecimientos.
>
> 2\. El sistema lo registra como administrador del paciente.
>
> 3\. El familiar envía invitaciones indicando el rol de cada persona.
>
> 4\. Cada invitado acepta la invitación y queda incorporado con su rol.
>
> 5\. El familiar vincula el wearable al perfil del paciente.

**Resultado:** El paciente queda creado, con su círculo de cuidado y su wearable asociado.

**Requisitos cubiertos:** RF-08 a RF-16

## **CU-02 --- Registrar mediciones y detectar una anomalía**

**Actor:** Sistema, wearable

**Precondición:** El paciente tiene un wearable vinculado y rangos normales configurados.

**Flujo principal:**

> 1\. La aplicación envía al servidor el lote de mediciones recogidas por el wearable.
>
> 2\. El sistema descarta las mediciones ya registradas y almacena las nuevas.
>
> 3\. El sistema compara cada medición con el rango normal configurado.
>
> 4\. Si alguna queda fuera de rango, genera una alerta y notifica a los usuarios correspondientes.
>
> 5\. El sistema recalcula el indicador diario de bienestar del paciente.

**Resultado:** Las mediciones quedan registradas y, si corresponde, se genera la alerta.

**Requisitos cubiertos:** RF-17, RF-20, RF-22, RF-44, RF-45

## **CU-03 --- Administrar una toma de medicamento**

**Actor:** Cuidadora

**Precondición:** Existe un plan de medicamentos vigente con tomas generadas para el día.

**Flujo principal:**

> 1\. El sistema avisa a la cuidadora a la hora de la toma.
>
> 2\. La cuidadora abre la toma y registra el resultado.
>
> 3\. Si la marca como omitida, el sistema exige un motivo.
>
> 4\. Si la pospone, el sistema valida que no exceda el plazo permitido.
>
> 5\. El sistema actualiza la adherencia del paciente.

**Flujo alternativo:** Si la toma no se confirma dentro de su plazo, el sistema la marca como omitida y alerta al familiar.

**Resultado:** La toma queda registrada y visible para el familiar.

**Requisitos cubiertos:** RF-28, RF-29, RF-30, RF-33

## **CU-04 --- Digitalizar una receta médica**

**Actor:** Cuidadora o médico

**Precondición:** El usuario tiene la receta en papel y acceso al paciente.

**Flujo principal:**

> 1\. El usuario fotografía la receta desde la aplicación.
>
> 2\. El sistema procesa la imagen y extrae los medicamentos, dosis y horarios detectados.
>
> 3\. El sistema presenta las sugerencias con su nivel de confianza para que el usuario las revise.
>
> 4\. El usuario corrige lo necesario y confirma.
>
> 5\. El sistema agrega los medicamentos al plan y guarda la imagen en el expediente.

**Flujo alternativo:** Si la imagen no es legible, el sistema informa el problema y solicita una nueva fotografía.

**Resultado:** El plan queda actualizado y la receta archivada como documento.

**Requisitos cubiertos:** RF-31, RF-24, RF-40

## **CU-05 --- Atender una emergencia**

**Actor:** Cuidadora o adulto mayor

**Precondición:** El paciente tiene al menos un familiar en su círculo de cuidado.

**Flujo principal:**

> 1\. El usuario activa el botón de emergencia y confirma la acción.
>
> 2\. El sistema crea una alerta crítica y la registra en el expediente con su hora.
>
> 3\. El sistema notifica de inmediato a todos los familiares del paciente.
>
> 4\. El sistema entrega los teléfonos de contacto para llamar desde la aplicación.
>
> 5\. Un familiar marca la alerta como atendida y luego la cierra con una nota.

**Flujo alternativo:** Si nadie atiende dentro del plazo, el sistema escala el aviso a los siguientes contactos definidos.

**Resultado:** La emergencia queda registrada, atendida y documentada en el historial.

**Requisitos cubiertos:** RF-48, RF-49, RF-51, RF-52

## **CU-06 --- Consultar el estado del paciente al asistente**

**Actor:** Familiar, cuidadora o médico

**Precondición:** El paciente tiene información registrada en su expediente.

**Flujo principal:**

> 1\. El usuario escribe una pregunta en lenguaje natural sobre el paciente.
>
> 2\. El sistema reúne la información del expediente que el rol del usuario puede ver.
>
> 3\. El sistema consulta al modelo de lenguaje y elabora la respuesta.
>
> 4\. El sistema entrega la respuesta indicando los datos en que se basa.

**Flujo alternativo:** El asistente nunca entrega información de otro paciente ni de datos que el rol no tenga permitido consultar.

**Resultado:** La conversación queda guardada en el historial del usuario.

**Requisitos cubiertos:** RF-56, RF-57, RF-59

## **CU-07 --- Comunicarse desde la vista del adulto mayor**

**Actor:** Adulto mayor

**Precondición:** El dispositivo del adulto mayor está vinculado a su perfil.

**Flujo principal:**

> 1\. El adulto mayor abre la conversación con su familia desde un acceso grande y simple.
>
> 2\. Dicta su mensaje por voz o grabar una nota de voz.
>
> 3\. El sistema transcribe o adjunta el audio y publica el mensaje en el canal.
>
> 4\. El sistema lee en voz alta los mensajes recibidos cuando el usuario lo solicita.

**Flujo alternativo:** Si no hay conexión, el mensaje se guarda en el dispositivo y se envía al recuperarla.

**Resultado:** El mensaje queda publicado y visible para el resto del círculo de cuidado.

**Requisitos cubiertos:** RF-53, RF-63, RF-64, RF-68, RF-80, RF-81
