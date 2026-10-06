# AgeCare — Análisis de Realidad y Decisiones de Diseño

**Proyecto APT · Capstone PTY4614 · DUOC UC — Sede San Andrés**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Metodología:** Enfoque Tradicional (Cascada) · **Entrega:** 04 de octubre (avance Fase 2)

---

## 1. Para qué sirve este documento

El modelo relacional y la normalización demuestran rigor técnico, pero un sistema de salud se
evalúa también por su **análisis de la realidad**: qué pasa cuando el mundo no se comporta como
el caso feliz. Este documento anticipa esas situaciones, explica dónde las sostiene el modelo,
y —cuando la tecnología tiene un límite— nombra la decisión de ingeniería de forma explícita.

El principio que guía el diseño: **el software no puede garantizar actos humanos físicos, pero
sí puede crear trazabilidad, responsabilidad y detección.** Donde no se puede prevenir, se
registra y se audita.

---

## 2. Escenarios del mundo real y cómo responde el modelo

### E1. Al paciente se le apaga el celular o el wearable se queda sin batería

**Qué pasa:** dejan de llegar lecturas de signos vitales.

**Cómo lo sostiene el modelo:**
- `wearables.last_sync_at` guarda la última sincronización. El sistema **no almacena un estado
  "conectado"**: lo calcula comparando `last_sync_at` con la hora actual. Esto evita un estado
  mentiroso que quede "pegado" en conectado cuando en realidad no hay señal.
- El umbral de inactividad vive en `system_parameters` (`wearable_offline_minutes = 120`), no
  en el código. Es configurable y auditable sin redesplegar.
- Superado el umbral, el motor genera una alerta `wearable_offline` (RF-44) para que la familia
  sepa que hay un hueco de datos, en vez de asumir silencio = todo bien.

**Decisión consciente:** el modelo **no distingue** entre "wearable apagado", "sin señal" y
"paciente se quitó el reloj". Las tres colapsan en `wearable_offline`. Distinguirlas exigiría
telemetría del dispositivo que el simulador de v1 no provee. Se documenta como simplificación
de alcance, no como omisión.

---

### E2. ¿A qué hora se registra realmente un medicamento? ¿Y si se marca tarde?

Este es el escenario donde más fácilmente se confunde "lo que pasó" con "lo que se anotó".

**El modelo distingue TRES momentos** en `scheduled_doses`:

| Columna | Significado | Ejemplo |
|---|---|---|
| `scheduled_at` | Cuándo **debía** administrarse (lo planifica el job). | 08:00 |
| `administered_at` | Cuándo se administró **realmente** al paciente (hecho clínico). | 08:40 |
| `logged_at` | Cuándo la cuidadora lo **registró** en la app (acto administrativo). | 23:00 |

Gracias a esta separación, el sistema puede responder preguntas que antes eran imposibles:
*"¿la pastilla se dio a tiempo, o solo se registró tarde?"* Con una sola columna de "hora", esa
distinción se pierde y la adherencia queda contaminada por el momento del papeleo.

Los `CHECK` refuerzan la coherencia:
- `ck_scheduled_doses_administered`: una dosis `taken` **debe** tener `administered_at`.
- `ck_scheduled_doses_admin_order`: no se puede administrar **antes** de la hora programada.

---

### E3. ¿Y si a la cuidadora le dio flojera y marca todo como "tomado" sin que sea verdad?

Esta es la pregunta de **dependencia humana**, y la respuesta honesta de ingeniería es:

> A nivel de base de datos **no se puede garantizar la veracidad de un acto presencial**.
> Ninguna tabla puede saber si la pastilla entró a la boca del paciente. Lo que el sistema SÍ
> hace es transformar el problema de *prevención* (imposible) en uno de *responsabilidad*
> (sí modelable).

Cómo lo sostiene el modelo:
- `scheduled_doses.logged_by` + `logged_at`: queda registrado **quién** declaró la dosis y
  **cuándo**, de forma asociada a su cuenta.
- `audit_log` (tabla **inmutable**, append-only con trigger que bloquea `UPDATE`/`DELETE`):
  si alguien edita el estado de una dosis o lo registra fuera de hora, queda un rastro que no
  se puede borrar. Cumple RNF-14 (trazabilidad clínica).
- La discordancia entre `administered_at` y `logged_at` (E2) es, además, una **señal detectable**:
  registros sistemáticamente tardíos o en lote delatan un patrón de negligencia que un reporte
  puede evidenciar.

**Conclusión defendible:** el límite entre lo que valida la tecnología y lo que depende de la
persona está **explícitamente trazado**. El sistema no finge prevenir lo que no puede; crea la
evidencia para auditar y rendir cuentas.

---

### E4. ¿Y si la cuidadora simplemente se olvida de administrar la dosis?

**Cómo lo sostiene el modelo:**
- La dosis existe en `scheduled_doses` **antes de ocurrir** (la genera el job). Esto es clave:
  sin la fila previa, una omisión sería invisible (no habría denominador para la adherencia).
- Si nadie confirma la dosis dentro de su ventana (`medications.grace_window_min`), el job la
  marca `missed` y dispara una alerta `missed_dose` al familiar (RF-33, RF-44).
- La alerta escala a los siguientes contactos si nadie la atiende, según
  `system_parameters.alert_escalation_minutes` y el orden de `emergency_contacts` (RF-52).

El olvido humano no se puede evitar, pero el sistema lo **detecta y lo comunica** en vez de
dejarlo pasar en silencio.

---

### E5. "El medicamento se da a una hora exacta, pero la vida real tiene ventanas"

- `medications.grace_window_min` define la tolerancia (por defecto 60 min) antes de considerar
  una dosis omitida. La hora programada no es un instante rígido.
- **Decisión de alcance:** los horarios (`medication_times.time_of_day`) son fijos en v1. Un
  esquema tipo "con el desayuno" (hora relativa a un evento del paciente) queda fuera del
  alcance de esta fase y se declara como mejora futura, no como vacío.

---

### E6. ¿Puedo saber cómo estuvo el paciente la semana pasada?

**Sí.** El indicador diario de bienestar (semáforo) se persiste en `wellbeing_snapshots`, una
fotografía por paciente y día. Antes se calculaba al vuelo y se perdía; ahora el expediente
tiene **memoria histórica** del bienestar y se pueden mostrar tendencias. Cada snapshot guarda
los conteos que lo justifican (`vitals_out_of_range`, `doses_missed`, `active_alerts`), de modo
que el estado del día es **auditable**, no un número mágico.

---

## 3. Decisiones de modelado teórico (lo que preguntará un DBA)

### D1. Eliminaron `patient_id` de `scheduled_doses` por 2FN. ¿No afecta el rendimiento?

Es un **trade-off consciente**. La 2FN exige eliminar la dependencia parcial (`patient_id`
dependía de `medication_id`, no de la PK). El costo es un `JOIN` adicional en la agenda del día,
cubierto por `ix_scheduled_doses_medication_time` y por el índice sobre `medications.patient_id`.
Para el volumen esperado (decenas de dosis por paciente/día) el impacto es despreciable. Si un
perfilado en producción mostrara un cuello de botella, se evaluaría una **desnormalización
controlada y documentada**, igual que la excepción de la PK de `vital_readings`. La normalización
es una guía de integridad, no un dogma que ignore el contexto.

### D2. `vital_readings` tiene PK compuesta `(id, measured_at)`. ¿No viola 2FN?

En sentido estricto sí: los atributos dependen solo de `id`. Pero `measured_at` está en la PK
**por un requisito técnico de PostgreSQL**: la columna de particionamiento de una tabla
`PARTITION BY RANGE` debe formar parte de la clave primaria. Es una **excepción técnica
documentada** en el propio constraint, no un error de diseño. El particionado por mes es lo que
permite cumplir RNF-07 (escala de la telemetría).

### D3. ¿Por qué `payload`, `meta` y `reasons` son `jsonb` si normalizaron todo lo demás?

Son datos de **atributos variables**: su estructura cambia según el tipo de alerta, el proveedor
del wearable o el estado del día. Normalizarlos exigiría una tabla de detalle por cada variante
sin ganar integridad, porque **no se consultan ni se cruzan**: solo se muestran. Es el uso
legítimo de `jsonb`, documentado como excepción a 1FN en cada columna. El `CHECK
jsonb_typeof(...) = 'array'` en `reasons` evita que degenere en basura.

### D4. ¿Cómo garantizan que un dato clínico no se altere sin dejar rastro?

Con `audit_log`, tabla **append-only** cuya inmutabilidad está forzada por un trigger que lanza
excepción ante cualquier `UPDATE` o `DELETE`. Es la diferencia entre "confiar en que nadie toca
los datos" y "poder demostrar quién tocó qué". Requisito no funcional en todo sistema HealthTech.

### D5. ¿Dónde está la lógica de negocio del freemium?

En `subscriptions`. Sin esta tabla, RF-73 ("bloquear funciones premium sin suscripción vigente")
no sería implementable y la métrica de conversión del plan de negocio no sería medible. El
índice parcial `ux_subscriptions_active_user` garantiza **una sola suscripción activa por
usuario** a nivel de base de datos, no solo en la aplicación. No se almacenan datos de tarjeta
(`provider_ref` es una referencia opaca a la pasarela): cumplimiento PCI por diseño.

---

## 4. Límites explícitos de la tecnología (honestidad de ingeniería)

| Situación del mundo real | ¿La tecnología la previene? | Qué hace el sistema |
|---|---|---|
| La pastilla no entró a la boca del paciente | ❌ No | Registra quién/cuándo la declaró (`logged_by`), audita cambios (`audit_log`) |
| La cuidadora registra tarde o en lote | ❌ No lo impide | Lo evidencia: discordancia `administered_at` vs `logged_at` |
| El wearable se apaga | ❌ No lo evita | Lo detecta por ausencia de `last_sync_at` y alerta |
| Alguien quiere borrar un registro incómodo | ✅ Sí lo impide | `audit_log` inmutable + soft delete en registros clínicos |
| Un vital fuera de rango clínico | ✅ Sí lo detecta | `vital_thresholds` + alerta `vital_out_of_range` |
| Dosis duplicada / lote reenviado | ✅ Sí lo impide | `UNIQUE` natural (idempotencia, RNF-08) |

El valor de este cuadro ante un evaluador: demuestra que el equipo **distingue** lo que la
ingeniería puede garantizar de lo que depende del factor humano, y diseñó para cada caso lo
máximo que la disciplina permite.

---

## 5. Resumen de robustez del modelo

- **Integridad referencial:** todas las FK con `ON DELETE RESTRICT` (política de conservación: no se borra físicamente, se desactiva para preservar el histórico).
- **Integridad de dominio:** `CHECK` de estados, rangos, coherencia temporal y enums cerrados.
- **Normalización:** hasta 2FN, con excepciones técnicas y de atributos variables documentadas.
- **Trazabilidad:** `audit_log` inmutable (RNF-14) + `logged_by`/`administered_at`.
- **Escalabilidad:** particionado mensual de `vital_readings` (RNF-07) e idempotencia (RNF-08).
- **Configurabilidad:** parámetros de negocio en `system_parameters`, fuera del código.
- **Memoria histórica:** `wellbeing_snapshots` conserva la evolución del bienestar.
- **Análisis de realidad:** los límites humanos están nombrados y gestionados, no ignorados.
