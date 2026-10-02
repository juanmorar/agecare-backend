__AgeCare__

Plataforma de cuidado de adultos mayores

__Objetivos generales y específicos de la plataforma y de sus componentes__

Wellq Co

Documento de definición de proyecto

Versión 1\.0 — 28 de agosto de 2026

__Contenido__

[__1\. Introducción	3__](#_heading=)

[__2\. Objetivos de la plataforma AgeCare	3__](#_heading=)

[2\.1 Objetivo general	3](#_heading=)

[2\.2 Objetivos específicos	3](#_heading=)

[__3\. Objetivos de los componentes	4__](#_heading=)

[3\.1 Aplicación móvil de usuarios	4](#_heading=)

[3\.2 Versión web de la aplicación	5](#_heading=)

[3\.3 Web de administración	5](#_heading=)

[3\.4 Módulo de música de la aplicación del adulto mayor \(Director Musical\)	5](#_heading=)

[__4\. Consideraciones finales	6__](#_heading=)

# __1\. Introducción__

AgeCare es una plataforma digital de cuidado de adultos mayores orientada a dar tranquilidad a las familias que cuidan a un ser querido a distancia\. La plataforma reúne en un solo lugar el estado de salud del adulto mayor —medido por un dispositivo vestible \(wearable\) y registrado por la persona cuidadora—, un sistema de alertas, herramientas de comunicación asistidas por inteligencia artificial y una vista propia para el adulto mayor, accesible y de voz primero, que lo mantiene conectado, acompañado y estimulado\.

La plataforma se articula como un único producto con datos compartidos del paciente y vistas diferenciadas por rol: el familiar observa el estado de salud y recibe alertas; la cuidadora opera el día a día y captura datos; el médico prescribe y ajusta el plan de medicamentos; y el adulto mayor participa activamente desde una interfaz radicalmente simple que incluye, entre otros, el módulo de creación musical «Director Musical»\.

El presente documento define el objetivo general y los objetivos específicos de la plataforma AgeCare, y detalla a continuación los objetivos de cada uno de sus componentes: la aplicación móvil de usuarios, la versión web de la aplicación, la web de administración y el módulo de música de la aplicación del adulto mayor\. Se elabora a partir del Documento de Funcionalidades v1, el Plan de Negocio, el Plan de Desarrollo v1, la Especificación de Endpoints de Backend v1 y la Especificación Técnica del Director Musical\.

# __2\. Objetivos de la plataforma AgeCare__

## __2\.1 Objetivo general__

Desarrollar una plataforma digital integral de cuidado de adultos mayores que centralice el monitoreo de salud, las alertas, la coordinación del cuidado y la comunicación entre familiares, cuidadores, médicos y el propio adulto mayor, con el fin de proporcionar a las familias que cuidan a distancia información confiable y en tiempo real sobre el bienestar de su ser querido, y al adulto mayor un medio accesible para mantenerse conectado, acompañado y activo\.

## __2\.2 Objetivos específicos__

1. Consolidar en un expediente único y compartido la información de salud del adulto mayor —signos vitales del wearable, adherencia a medicamentos, observaciones de la cuidadora, incidentes y documentos médicos—, presentada mediante un semáforo de bienestar diario por paciente y con soporte multi\-paciente\.
2. Implementar un sistema de alertas en tiempo real, con notificaciones push y umbrales configurables, que detecte y comunique los eventos críticos del cuidado: caída detectada, signo vital fuera de rango y medicamento no administrado, incluyendo un flujo de acción inmediata ante caídas y un botón SOS\.
3. Gestionar el ciclo completo de la medicación: definición del plan por la cuidadora o el médico, digitalización de recetas mediante OCR, alarmas de tomas, confirmación de dosis y visualización de la adherencia por parte del familiar\.
4. Facilitar la comunicación y la coordinación del círculo de cuidado mediante un chat contextual al paciente \(texto, voz y foto\) y un asistente de inteligencia artificial capaz de interpretar el expediente y responder preguntas en lenguaje natural\.
5. Ofrecer al adulto mayor una experiencia propia, accesible y de voz primero, que lo integre como usuario activo de la plataforma: comunicación con su familia, fotos compartidas, entretenimiento curado y creación musical mediante el módulo Director Musical\.
6. Definir un modelo de roles y permisos \(familiar, cuidadora, médico, adulto mayor\) que separe la observación de la operación, garantizando que cada usuario acceda únicamente a las funciones e información propias de su rol\.
7. Sustentar la adopción y la sostenibilidad del producto mediante un modelo freemium en el que las funciones esenciales de cuidado son gratuitas, el adulto mayor nunca paga y la monetización se realiza a través de planes premium para familias y proveedores, con un marketplace de cuidadoras y artículos de apoyo como vitrina de descubrimiento\.
8. Garantizar la seguridad, privacidad y disponibilidad de los datos de salud tratados por la plataforma, mediante autenticación robusta, control de acceso por roles y una infraestructura en la nube escalable que soporte el crecimiento previsto en el plan de negocio\.

# __3\. Objetivos de los componentes__

## __3\.1 Aplicación móvil de usuarios__

Aplicación para iOS y Android que constituye el punto de acceso principal a la plataforma, con vistas diferenciadas para el familiar, la cuidadora, el médico y el adulto mayor\. Su objetivo general es poner el centro de mando del cuidado en el bolsillo de cada rol, con la promesa de saber de un vistazo que el ser querido está bien\.

1. Proporcionar al familiar un inicio de tipo «Hoy» con el semáforo de bienestar, las alertas activas, el resumen de signos vitales, los medicamentos del día y la última observación, con acceso al historial completo de salud\.
2. Ofrecer a la cuidadora una vista operativa orientada a la captura: check\-in del día, confirmación de dosis, registro de observaciones e incidentes, gestión de tareas y relevo de turno\.
3. Entregar las alertas y notificaciones push de la plataforma con la menor latencia posible, incluyendo el flujo crítico de caídas y el botón SOS\.
4. Integrar el hub de comunicación —chat de coordinación y asistente de IA— y la vista accesible del adulto mayor, con interacción por voz, mensajes familiares, galería de fotos y entretenimiento\.
5. Incorporar la vinculación y sincronización de wearables para la ingesta de signos vitales, así como la digitalización de recetas mediante la cámara y OCR\.

## __3\.2 Versión web de la aplicación__

Versión de la aplicación de usuarios accesible desde el navegador, que replica las funcionalidades de la app móvil para los roles familiar, cuidadora y médico\. Su objetivo general es garantizar el acceso a la plataforma desde cualquier dispositivo con navegador, sin necesidad de instalación\.

1. Ofrecer en el navegador las funciones esenciales de la app de usuarios: monitoreo del paciente, centro de alertas, gestión de medicamentos, comunicación y consulta del expediente\.
2. Facilitar el trabajo prolongado en pantalla grande para los roles que lo requieren, en particular la revisión del expediente por el médico y la elaboración de reportes por la cuidadora profesional\.
3. Servir de vía de acceso inmediata para usuarios nuevos o esporádicos \(por ejemplo, un familiar invitado\), reduciendo la barrera de entrada a la plataforma\.
4. Mantener paridad de datos y de sesión con la aplicación móvil, consumiendo la misma API y respetando el mismo modelo de roles y permisos\.

## __3\.3 Web de administración__

Panel interno de administración de la plataforma, destinado al equipo de operaciones de Wellq Co\. Su objetivo general es asegurar la operación, el soporte y la calidad del contenido y de los catálogos de AgeCare\.

1. Administrar usuarios, cuentas y roles de la plataforma, dando soporte a la resolución de incidencias de los usuarios finales\.
2. Curar y gestionar el contenido de entretenimiento del adulto mayor y los parámetros de configuración del sistema\.
3. Mantener los catálogos del marketplace \(cuidadoras y artículos de apoyo\) y moderar reseñas y perfiles publicados\.
4. Proporcionar dashboards operativos y de negocio para el seguimiento de la adopción, el uso y las métricas clave de la plataforma, así como la gestión de los aspectos legales \(términos, privacidad\)\.

## __3\.4 Módulo de música de la aplicación del adulto mayor \(Director Musical\)__

Módulo de creación musical integrado en la experiencia del adulto mayor, pensado para tablet: la persona mayor crea música dirigiendo con gestos de las manos frente a la cámara, sobre una escala pentatónica que garantiza un resultado siempre armonioso\. Su objetivo general es estimular cognitiva y emocionalmente al adulto mayor a través de la creación musical activa, sin barreras técnicas ni credenciales, y convertir esa actividad en un vínculo con su familia y en información útil para sus cuidadores\.

1. Permitir la creación musical mediante gestos naturales de las manos \(la posición controla tempo e intensidad\), con generación y renderizado del audio íntegramente en el dispositivo y funcionamiento offline\-first\.
2. Grabar y conservar las canciones creadas \(eventos musicales y audio M4A\), sincronizándolas con el backend central cuando hay conexión, con idempotencia y reintentos garantizados\.
3. Eliminar toda barrera de acceso para el adulto mayor: la cuenta la crea y administra el cuidador o la institución, y el dispositivo se vincula mediante un código simple, sin que la persona mayor introduzca nunca credenciales\.
4. Compartir las creaciones con la familia mediante enlaces seguros de escucha, reforzando el vínculo afectivo y el sentido de logro del adulto mayor\.
5. Registrar métricas de uso por sesión \(tiempo activo, detección de manos, canciones grabadas, tempo e intensidad medios\) que permitan a cuidadores y terapeutas dar seguimiento a la actividad con fines terapéuticos\.

# __4\. Consideraciones finales__

Los objetivos aquí definidos corresponden a la versión 1 de la plataforma y a su alcance documentado\. Constituyen el marco de referencia para la planificación, el desarrollo y la evaluación del proyecto: todo requisito funcional debe poder trazarse a uno de los objetivos específicos enunciados, y el cumplimiento de estos deberá verificarse en los hitos definidos en el Plan de Desarrollo v1 \(núcleo de salud, piloto con usuarios reales y publicación en tiendas\)\. Las capacidades previstas para fases posteriores —marketplace transaccional, integración de wearables comerciales y expansión regional— se incorporarán a revisiones futuras de este documento\.
