# AgeCare — Historias de Usuario

**Proyecto APT · Capstone PTY4614 · DUOC UC — Sede San Andrés**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Metodología:** Enfoque Tradicional (Cascada) · **Entrega:** 04 de octubre (avance Fase 2)

---

## 1. Propósito

Este documento traduce los requisitos funcionales del **ERS simplificado** (Fase 1) a
**historias de usuario** con criterios de aceptación verificables. Cada historia referencia
los **RF-XX** que la originan y, cuando aplica, el **caso de uso (CU-01 … CU-07)** del ERS que
la contextualiza. No introduce requisitos nuevos: es una vista orientada al usuario del mismo
alcance ya aprobado.

Formato: *Como [actor] quiero [acción] para [beneficio]*.
Estado: ✅ soportada por el modelo definitivo · ⏳ etapa posterior del cronograma.

---

## 2. Historias del núcleo de salud (avance 04 de octubre)

### Autenticación y cuentas — *CU-01*

**HU-01 · Registro de cuenta** — ✅ · *RF-01*
Como **familiar** quiero **crear una cuenta con mi correo y contraseña** para **empezar a usar la plataforma**.
- Un correo no registrado crea la cuenta y devuelve sesión iniciada.
- Un correo ya registrado se rechaza sin crear duplicado.
- La contraseña se guarda con hash, nunca en texto plano (RNF-10).

**HU-02 · Inicio de sesión** — ✅ · *RF-02*
Como **usuario** quiero **iniciar sesión** para **acceder a mis pacientes**.
- Credenciales válidas devuelven la sesión y mis pacientes con mi rol en cada uno.
- Credenciales inválidas no revelan si el correo existe.

**HU-03 · Sesión persistente y segura** — ✅ · *RF-03, RF-04*
Como **usuario** quiero **que mi sesión se mantenga sola de forma segura** para **no re-loguearme ni quedar expuesto**.
- La sesión se renueva automáticamente (refresh rotatorio, RNF-11).
- Al cerrar sesión deja de notificar a ese dispositivo.

**HU-04 · Recuperar contraseña** — ✅ · *RF-05*
Como **usuario** quiero **recuperar mi contraseña** para **no perder el acceso**.
- Se restablece por correo y se cierran todas las sesiones abiertas.

**HU-05 · Gestionar mi perfil** — ✅ · *RF-06, RF-07*
Como **usuario** quiero **ver y editar mi perfil y registrar mi dispositivo** para **mantener mis datos y recibir notificaciones**.
- Puedo actualizar nombre, teléfono, foto e idioma.
- Mi dispositivo queda registrado para avisos.

### Pacientes y círculo de cuidado — *CU-01*

**HU-06 · Crear paciente** — ✅ · *RF-08*
Como **familiar** quiero **crear el perfil de mi ser querido** para **empezar a cuidarlo en la plataforma**.
- Al crear el paciente quedo como administrador.
- El paciente aparece en mi selector.

**HU-07 · Ver mis pacientes** — ✅ · *RF-09, RF-23*
Como **familiar** quiero **ver todos mis pacientes y su estado** para **saber de un vistazo quién necesita atención**.
- Con más de un paciente, veo un resumen por cada uno.
- Solo veo pacientes donde tengo acceso vigente.

**HU-08 · Administrar datos del paciente** — ✅ · *RF-10*
Como **familiar administrador** quiero **modificar los datos del paciente** para **mantener su información al día**.

**HU-09 · Invitar al círculo de cuidado** — ✅ · *RF-11, RF-12, RF-13*
Como **familiar administrador** quiero **invitar a la cuidadora y al médico** para **que operen y revisen el expediente**.
- La invitación es un enlace de un solo uso con vencimiento (7 días).
- Un enlace usado o vencido se rechaza.
- Aceptar la invitación crea la membresía con el rol correcto.

**HU-10 · Quitar a un miembro** — ✅ · *RF-14*
Como **familiar administrador** quiero **quitar a un miembro** para **controlar quién accede al expediente**.
- No puedo eliminar al administrador.
- La baja conserva el historial de pertenencia.

**HU-11 · Vincular wearable** — ✅ · *RF-15, RF-16*
Como **familiar o cuidadora** quiero **vincular el wearable del paciente** para **recibir sus signos vitales**.
- Solo un wearable activo a la vez; vincular uno nuevo desvincula el anterior.
- Veo última medición, batería y si lleva mucho sin enviar datos.

### Salud y signos vitales — *CU-02*

**HU-12 · Ingesta de mediciones del wearable** — ✅ · *RF-17*
Como **sistema** quiero **recibir lotes de mediciones del wearable** para **alimentar el expediente sin duplicar datos**.
- Un lote de 500 mediciones se procesa en < 1 s (RNF-01).
- Las mediciones ya registradas se descartan (RNF-08).

**HU-13 · Registrar vital manual** — ✅ · *RF-18*
Como **cuidadora** quiero **registrar presión/temperatura/glucosa a mano** para **complementar el wearable**.

**HU-14 · Consultar tendencias** — ✅ · *RF-19, RF-20*
Como **familiar** quiero **ver el historial de un signo vital y su último valor** para **entender cómo evoluciona mi ser querido**.
- Puedo agrupar por hora, día o semana.
- Cada último valor indica si está dentro del rango.

**HU-15 · Configurar umbrales** — ✅ · *RF-21*
Como **familiar o médico** quiero **definir el rango normal de cada vital** para **que las alertas sean pertinentes**.
- No se acepta un mínimo mayor o igual al máximo.

**HU-16 · Indicador diario de bienestar** — ✅ · *RF-22*
Como **familiar** quiero **un indicador diario de bienestar** para **saber de un vistazo cómo está el paciente**.
- Se calcula con mediciones, adherencia y eventos del día, mostrando los motivos.

### Medicamentos y adherencia — *CU-03, CU-04*

**HU-17 · Definir el plan de medicamentos** — ✅ · *RF-24, RF-25*
Como **cuidadora o médico** quiero **crear el plan de medicación** para **organizar las tomas del paciente**.
- Indico dosis, horarios, días y vigencia.
- El familiar ve el plan en solo lectura.

**HU-18 · Editar y descontinuar medicamento** — ✅ · *RF-26, RF-27*
Como **cuidadora o médico** quiero **modificar o descontinuar un medicamento** para **ajustar el tratamiento sin perder el historial**.
- La edición regenera solo tomas futuras.
- Descontinuar cancela futuras y conserva lo administrado.

**HU-19 · Agenda de tomas del día** — ✅ · *RF-28, RF-32*
Como **cuidadora** quiero **ver las tomas del día** para **administrarlas a tiempo**.
- Las tomas del día siguiente se generan automáticamente en la zona horaria del paciente.
- Se identifica la próxima toma pendiente.

**HU-20 · Registrar administración** — ✅ · *RF-29, RF-33* · *CU-03*
Como **cuidadora** quiero **marcar cada toma como administrada, pospuesta u omitida** para **llevar la adherencia**.
- Omitir exige motivo; posponer tiene un límite de tiempo.
- Una toma no confirmada en su plazo pasa a omitida y alerta al familiar.

**HU-21 · Ver adherencia** — ✅ · *RF-30*
Como **familiar** quiero **ver la adherencia** para **saber si mi ser querido toma sus medicinas**.
- Veo el porcentaje por rango, por medicamento y por día; sin editar el plan.

**HU-22 · Digitalizar receta (OCR)** — ⏳ · *RF-31* · *CU-04*
Como **cuidadora o médico** quiero **fotografiar una receta y que se extraigan los medicamentos** para **cargar el plan más rápido**.
- Las sugerencias se revisan y corrigen antes de confirmar.

### Alertas y emergencias — *CU-05*

**HU-23 · Recibir alertas** — ✅ · *RF-44, RF-45, RF-46*
Como **familiar** quiero **recibir alertas** para **enterarme al instante de un evento crítico**.
- Se generan por caída, vital fuera de rango, toma no administrada y wearable sin datos.
- Una caída avisa en < 10 s (RNF-04); no se repiten por la misma causa en el intervalo.

**HU-24 · Centro de alertas** — ✅ · *RF-47, RF-48, RF-49*
Como **familiar o cuidadora** quiero **un centro de alertas** para **revisar lo ocurrido y atender lo pendiente**.
- Puedo filtrar por estado y ver no leídas.
- Puedo atender (detiene recordatorios) y cerrar con nota.

**HU-25 · Preferencias de notificación** — ✅ · *RF-50*
Como **usuario** quiero **elegir qué notificaciones recibir** para **no saturarme**, sin poder desactivar caída ni emergencia.

**HU-26 · Botón de emergencia** — ✅ · *RF-51, RF-52* · *CU-05*
Como **cuidadora o adulto mayor** quiero **un botón de emergencia** para **pedir ayuda inmediata**.
- Genera alerta crítica, avisa a todos los familiares y entrega los teléfonos de contacto.
- Si nadie atiende en el plazo, escala a los siguientes contactos.

---

## 3. Historias de etapas posteriores (Fase 2 — resto del cronograma)

Declaradas para trazabilidad completa del ERS. Su soporte en el modelo se incorpora según la
Carta Gantt; el diseño del núcleo las admite por extensión.

| HU | Actor | Historia | RF | CU |
|---|---|---|---|---|
| HU-27 | Cuidadora | Registrar observaciones e incidentes del día | RF-34, RF-36 | — |
| HU-28 | Cuidadora/Familiar | Dejar y leer notas de relevo | RF-37 | — |
| HU-29 | Adulto mayor | Registrar cómo me siento (check-in) | RF-38 | — |
| HU-30 | Todos | Subir y consultar documentos médicos | RF-39…43 | — |
| HU-31 | Todos | Conversar sobre el paciente (texto/voz/foto) | RF-53…55 | CU-07 |
| HU-32 | Familiar | Preguntar al asistente IA sobre el expediente | RF-56…59 | CU-06 |
| HU-33 | Adulto mayor | Ver y reaccionar a fotos de la familia | RF-60, RF-61 | — |
| HU-34 | Adulto mayor | Escuchar entretenimiento y mensajes en voz alta | RF-62, RF-63 | — |
| HU-35 | Adulto mayor | Comunicarse por dictado de voz | RF-64 | CU-07 |
| HU-36 | Adulto mayor | Crear y compartir música (Director Musical) | RF-65…69 | — |
| HU-37 | Cuidadora | Operar su día (vista, tareas, perfil, reportes) | RF-70…74 | — |
| HU-38 | Familiar | Explorar el marketplace de cuidadoras y productos | RF-75…79 | — |
| HU-39 | Todos | Operar sin conexión y sincronizar | RF-80…82 | — |

---

## 4. Resumen de cobertura

| Grupo | Historias | Estado |
|---|---|---|
| Núcleo de salud (auth, pacientes, vitals, medicación, alertas/emergencia) | HU-01 a HU-26 | ✅ 25 soportadas / 1 ⏳ (OCR, HU-22) |
| Bitácora, archivos, comunicación, IA, adulto mayor, cuidadora pro, marketplace, offline | HU-27 a HU-39 | ⏳ Fase 2 (resto del cronograma) |

**26 historias del núcleo de salud derivadas directamente de los RF del ERS; 25 ya soportadas
por el modelo de datos definitivo. 13 historias adicionales declaradas y trazadas para el
resto de la Fase 2.**
