relo__Suite de Cuidado de Adultos Mayores__

Documento de Funcionalidades — Versión 1

*Una app, vistas por rol · Multi\-paciente · Centrada en la tranquilidad del familiar*

Rol: Diseño de producto

Fecha: 15 de junio de 2026

# Contenido

# 1\. Visión del producto

La suite es un centro de mando tranquilizador para el familiar que cuida a un adulto mayor a distancia\. Reúne en un solo lugar el estado de salud del paciente \(medido por un wearable y registrado por la cuidadora\), una vitrina para encontrar apoyo, y un espacio de comunicación: con una IA que interpreta el historial y con las personas que rodean al paciente\.

El usuario principal es el familiar \(hijo o hija\): observa, recibe alertas y toma decisiones\. La cuidadora opera el día a día: captura datos y observaciones\. El médico prescribe\. El adulto mayor es un usuario activo con una vista propia, accesible, para mantenerse conectado y acompañado\. La promesa central es la paz mental: saber, de un vistazo, que el ser querido está bien\.

Esta versión 1 prioriza el monitoreo, las alertas y la comunicación\. El marketplace es una vitrina \(sin transacciones\), y el rol médico participa de forma acotada \(prescripción de medicamentos\)\.

# 2\. Personas y roles

La app es un solo producto que muestra vistas distintas según el rol de quien entra\. Los datos del paciente son compartidos; lo que cambia es la intención de cada pantalla\.

__Rol__

__Qué hace en la app__

Familiar \(principal\)

Vigila el estado del paciente, recibe alertas, consulta el historial, pregunta al asistente IA, coordina con la cuidadora y explora el marketplace\. Crea la cuenta e invita a los demás\.

Cuidadora

Captura el día a día: confirma medicamentos administrados, registra observaciones, verifica la sincronización del wearable\. Configura el plan de medicamentos\.

Médico

Prescribe y ajusta el plan de medicamentos; puede revisar el expediente\. Participación acotada en v1\.

Adulto mayor

Usuario activo con una vista propia, simple y accesible: envía mensajes de voz o texto a la familia, ve las fotos que le comparten, y lee o escucha chistes y noticias\. Porta el wearable\.

# 3\. Arquitectura de navegación

La vista del familiar se organiza en una barra de navegación inferior con cinco entradas\. Dos elementos son persistentes en la parte superior de toda la app: el selector de paciente y el centro de alertas \(campana\)\.

__Entrada__

__Propósito__

Inicio / Hoy

Vistazo del bienestar del día por paciente: semáforo, alertas, resumen de vitals, medicamentos de hoy y última observación\.

Salud

El expediente: vitals con tendencias, plan de medicamentos y adherencia, bitácora de observaciones y documentos\.

Comunicación

Hub con dos pestañas: Asistente IA \(preguntas sobre el historial\) y Mensajes \(chat con la familia y la cuidadora\)\.

Marketplace

Vitrina de cuidadoras y de artículos de apoyo\. Sin pagos ni agenda en v1\.

Más

Pacientes, gestión de roles e invitaciones, ajustes y configuración de notificaciones\.

Vista de la cuidadora: el Inicio se invierte de vigilar a capturar\. Su pantalla principal es un check\-in del día orientado a la acción\. Tiene un modelo de planes gratis/premium\. Se detalla en la sección 8\.

Vista del adulto mayor: es radicalmente más simple\. No usa la barra inferior; presenta unos pocos mosaicos grandes \(Familia, Fotos, Entretenimiento\) con diseño accesible y voz primero\. Se detalla en la sección 7\.

# 4\. Sección de Salud — Estado del paciente

Responde a la pregunta central del familiar: ¿cómo está hoy? Combina lo que mide el wearable, lo que registra la cuidadora y lo que prescribe el médico\.

## 4\.1 Inicio / Hoy

- Semáforo de bienestar del día por paciente \(bien / regular / requiere atención\), calculado a partir de vitals, adherencia y eventos\.
- Cuando hay más de un paciente, una tarjeta\-semáforo por cada uno para ver de un vistazo quién necesita atención\.
- Banda de alertas activas en la parte superior \(caída, vital fuera de rango, medicamento no tomado\)\.
- Tarjetas resumen: vitals clave del wearable, estado de medicamentos de hoy y la última observación de la cuidadora\.
- Acceso directo a preguntar al asistente desde cualquier tarjeta\.

## 4\.2 Vitals del wearable

Cada grupo de vitals se muestra como tarjeta con valor actual, mini\-gráfica de tendencia y umbral de alerta configurado\.

__Vital__

__Visualización__

Ritmo cardíaco

Frecuencia en reposo y a lo largo del día; tendencia semanal/mensual\.

Oxígeno \(SpO2\)

Saturación con umbral mínimo configurable y marca de lecturas bajas\.

Sueño y actividad

Horas de sueño, pasos y tiempo sedentario; patrones por día\.

Detección de caídas

Línea de tiempo de eventos \(no métrica continua\); cada caída abre un flujo de acción inmediata\.

- Estado de sincronización del wearable visible \(última lectura, batería\) para detectar lagunas de datos\.

## 4\.3 Medicamentos y adherencia

- Plan de medicamentos: medicina, dosis y horario\. Lo configura la cuidadora o el médico, o se importa digitalizando una receta \(foto/OCR con sugerencia del plan\)\.
- Registro de adherencia: la cuidadora marca cada dosis administrada; la app muestra tomadas, pendientes y omitidas del día\.
- El familiar visualiza la adherencia pero no edita el plan \(separación de roles: observar vs\. operar\)\.
- Una dosis no tomada dentro de su ventana genera alerta\.

## 4\.4 Observaciones y documentos

- Bitácora de observaciones de la cuidadora \(texto y, opcionalmente, foto\): ánimo, apetito, incidencias, notas del día\.
- Repositorio de documentos médicos \(recetas, estudios, indicaciones\) asociados al expediente\.
- Todo el contenido del expediente es consultable por el asistente IA\.

# 5\. Sección de Marketplace — Vitrina de apoyo

En v1 es una vitrina de descubrimiento: mostrar y comparar opciones, sin pagos ni agenda dentro de la app\. El cierre \(contacto o compra\) ocurre fuera\.

## 5\.1 Cuidadoras

- Listado y búsqueda de cuidadoras con filtros \(zona, especialidad, disponibilidad, idioma\)\.
- Perfil: experiencia, especialidad, reseñas y calificaciones, certificaciones\.
- Acción final: Contactar o Ver más \(sin transacción en la app\)\.

## 5\.2 Artículos de apoyo

- Catálogo navegable por categoría \(movilidad, monitoreo, seguridad en el hogar, cuidado diario\)\.
- Ficha de producto: descripción, fotos, rango de precio referencial\.
- Acción final: enlace a contacto o sitio externo para adquirir\.

*Nota de diseño: aunque sea vitrina, conviene dejar preparada la base para fases futuras \(agendar, contratar y pagar dentro de la app\)\.*

# 6\. Sección de Comunicación

Un único hub para hablar, con dos pestañas\. Conviven la conversación con la IA \(sobre datos\) y la conversación entre personas \(coordinación\)\.

## 6\.1 Asistente IA \(sobre el historial\)

- Chat en lenguaje natural que lee el expediente del paciente y responde: ¿cómo ha dormido esta semana?, ¿se ha saltado alguna medicina?, resúmeme cómo estuvo mamá en mayo\.
- Conectado a cada dato del expediente: desde cualquier tarjeta de Salud se puede preguntar al asistente sobre esto\.
- Hace que el expediente detallado sea menos intimidante: traduce datos en respuestas simples\.

## 6\.2 Mensajes \(entre personas\)

- Chat de coordinación entre familiares y la cuidadora \(ej\. ¿quién la lleva al médico el jueves?, papá durmió mal anoche\)\.
- Ligado al contexto del paciente; con varios pacientes, las conversaciones se separan por persona\.
- Se puede invocar a la IA dentro del chat humano \(*@asistente, ¿cómo van sus vitals esta semana?*\) para traer un dato a la conversación\.
- El adulto mayor participa en este chat desde su vista accesible, con mensajes de voz o texto por dictado \(ver sección 7\)\.

# 7\. Vista del adulto mayor — Acompañamiento

El adulto mayor es un usuario activo, pero su experiencia es distinta a la del familiar: prioriza la accesibilidad y la compañía por encima de los datos\. El objetivo es que se mantenga conectado con su familia y entretenido, con el mínimo esfuerzo\.

## 7\.1 Principios de diseño

- Voz primero: dictar mensajes y escuchar contenido en voz alta como modo principal de interacción\.
- Tipografía grande, alto contraste y botones amplios; objetivos táctiles generosos\.
- Pocos mosaicos grandes en lugar de una barra de navegación densa; mínima cantidad de pasos\.
- Lenguaje cálido y simple; evitar tecnicismos y menús anidados\.

## 7\.2 Familia \(chat\)

- Enviar y recibir mensajes en el chat compartido con la familia\.
- Mensajes de voz: grabar y reproducir notas de voz con un botón grande\.
- Escribir por dictado \(voz a texto\) o por teclado, según prefiera\.
- Lectura en voz alta de los mensajes recibidos\.

## 7\.3 Fotos de la familia

- Galería de fotos que los familiares comparten desde su vista\.
- Modo presentación \(slideshow\) para verlas de forma sencilla\.
- Reaccionar a una foto de forma simple \(ej\. un corazón o una nota de voz\)\.

## 7\.4 Entretenimiento \(chistes y noticias\)

- Chistes y noticias disponibles en modo leer o escuchar \(lectura en voz alta / audio\)\.
- Contenido apropiado y curado; tono ligero y compañía diaria\.
- Controles simples de reproducción \(escuchar, pausar, siguiente\)\.

## 7\.5 Check\-in opcional

- ¿Cómo me siento hoy? con caritas o botones grandes \(bien / regular / mal\)\.
- Su respuesta alimenta la bitácora de observaciones del expediente, dándole voz propia en su cuidado\.

*Diseño de dos caras: la familia cura las fotos y conversa desde su vista; el adulto mayor recibe, escucha y participa desde la suya\. El mismo chat y la misma galería, con interfaces adaptadas a cada rol\.*

# 8\. Vista de la cuidadora — Operación diaria

La cuidadora es quien alimenta el sistema\. Su experiencia invierte la del familiar: en vez de vigilar, opera\. La pantalla principal es un check\-in del día orientado a la acción, con captura rápida y poca fricción\. Atiende a un adulto mayor por vez\. Tiene un modelo de planes gratis/premium\.

## 8\.1 Inicio / Check\-in del día

- Encabezado con el adulto mayor a su cargo y el estado general del día\.
- Próxima toma de medicamento destacada, con cuenta regresiva\.
- Lista de tareas del día \(medicamentos, alimentación, higiene, actividad\) marcable a medida que se cumplen\.
- Acciones rápidas: añadir observación, registrar un vital manual, tomar foto\.
- Botón de emergencia / SOS siempre visible\.

## 8\.2 Registro de información del adulto mayor

- Confirmar medicamentos administrados \(marcar cada dosis\)\.
- Registrar observaciones del día \(ánimo, apetito, sueño, incidencias\) en texto o con foto\.
- Registrar vitals manuales \(ej\. presión, temperatura, glucosa\) como complemento al wearable o cuando no lo hay\.
- Registrar incidentes \(ej\. una caída presenciada\) con hora y detalle\.
- Notas de relevo entre turnos, para que la siguiente cuidadora retome el contexto\.

## 8\.3 Alarma de medicamentos

- Alarma push a la hora de cada dosis, según el plan de medicamentos\.
- Recordatorio persistente hasta que se confirme la administración\.
- Cada dosis se marca como administrada, pospuesta u omitida \(con motivo\)\.
- Si no se confirma dentro de su ventana, se genera una alerta al familiar\.

## 8\.4 Comunicación con la familia

- Chat con la familia \(texto y voz\) ligado al adulto mayor\.
- Enviar fotos del adulto mayor al grupo familiar __\(Premium\)__\.

## 8\.5 Emergencia / SOS

- Botón de acceso rápido, siempre disponible, ante un incidente\.
- Avisa al familiar y, opcionalmente, permite llamar a emergencias\.
- El evento queda registrado en el expediente con hora\.

## 8\.6 Profesional y trabajo

- Perfil profesional: experiencia, certificaciones, reseñas y calificaciones\.
- Perfil destacado / mayor visibilidad en el marketplace __\(Premium\)__\.
- Ofertas de trabajo de cuidado: listado / vitrina; el contacto ocurre fuera de la app __\(Premium\)__\.
- Historial y reportes extendidos: historial largo, exportar reportes y estadísticas de su trabajo __\(Premium\)__\.

## 8\.7 Planes: gratis vs\. premium

Las funcionalidades de cuidado del día a día son gratis; las que amplían comunicación, oportunidades y reportes son premium\. El upgrade se ofrece de forma contextual donde aparece cada función premium\.

__Funcionalidad__

__Gratis__

__Premium__

Check\-in y tareas del día

Sí

Sí

Registro de información \(medicamentos, observaciones, vitals, incidentes\)

Sí

Sí

Alarma de medicamentos

Sí

Sí

Chat de texto/voz con la familia

Sí

Sí

Emergencia / SOS

Sí

Sí

Enviar fotos al grupo familiar

—

Sí

Ofertas de trabajo

—

Sí

Perfil profesional destacado

—

Sí

Historial y reportes extendidos

—

Sí

# 9\. Pilares transversales

## 9\.1 Multi\-paciente

- Una cuenta de familiar puede seguir a varios adultos mayores \(ej\. papá y mamá\)\.
- Selector de paciente persistente en la parte superior \(avatar \+ nombre, tocable para cambiar\)\.
- Inicio muestra una tarjeta\-semáforo por paciente cuando hay más de uno\.

## 9\.2 Alertas \(pilar central\)

Las alertas son el principal valor para el familiar y se tratan como elemento de primera clase\.

- Notificaciones push además de la vista dentro de la app\.
- Umbrales configurables por vital \(ej\. SpO2 mínimo, rango de ritmo cardíaco\)\.
- Centro de alertas propio \(icono de campana siempre visible\) con historial de alertas\.
- __Caídas: __alerta crítica en tiempo real con flujo de acción inmediata \(llamar a la cuidadora / a emergencias\)\.
- Tipos de alerta en v1: caída detectada, vital fuera de rango y medicamento no tomado\.

## 9\.3 Onboarding y roles

- El familiar crea la cuenta y el perfil del paciente\.
- El familiar invita a la cuidadora \(y al médico\) mediante invitación\.
- Vinculación del wearable al perfil del paciente durante la configuración\.
- Permisos por rol: el familiar observa, la cuidadora opera, el médico prescribe, el adulto mayor se comunica y se entretiene\.

# 10\. Alcance de la versión 1

## Incluido

- Monitoreo de salud \(vitals, medicamentos/adherencia, observaciones, documentos\)\.
- Sistema de alertas central con push, umbrales y flujo crítico de caídas\.
- Hub de Comunicación: Asistente IA \+ Mensajes \(familiares, cuidadora y adulto mayor\)\.
- Vista del adulto mayor: chat con voz/texto, fotos de la familia y entretenimiento \(chistes y noticias\)\.
- Vista de la cuidadora: check\-in del día, registro de información, alarma de medicamentos, SOS y modelo freemium \(foto al grupo familiar, ofertas de trabajo, perfil destacado y reportes extendidos como premium\)\.
- Marketplace como vitrina \(cuidadoras y artículos\)\.
- Multi\-paciente y onboarding por invitación\.

## Fuera de alcance \(fases futuras\)

- Transacciones en el marketplace \(agendar, contratar, pagar\)\.
- Rol médico ampliado \(consultas, telemedicina, indicaciones completas\)\.
- Servicios médicos a domicilio y exámenes\.

# 11\. Preguntas abiertas para la siguiente conversación

- Que wearable\(s\) integraremos y como gestionamos la sincronizacion y los huecos de datos?
- Como se calcula exactamente el semaforo de bienestar \(que pondera\)?
- Privacidad y consentimiento de datos de salud: que requisitos aplican en nuestra region?
- Que define el contacto de una cuidadora en el marketplace \(chat, telefono, formulario\)?
- Entretenimiento del adulto mayor: de que fuentes vienen las noticias y los chistes, y como se curan?
- Necesita el adulto mayor un dispositivo propio \(tablet, telefono\) y como es su onboarding asistido por la familia?
