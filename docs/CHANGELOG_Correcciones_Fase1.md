# Registro de Correcciones — Documento de Fase 1 (Guía 1.5)

**Proyecto APT · Capstone PTY4614 · DUOC UC — Grupo 1**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Documento afectado:** `1.5_GuiaEstudiante_Fase 1_Definicion Proyecto APT (Español)`

---

## 1. Propósito

Este registro documenta, en honor a la trazabilidad propia de la metodología en cascada
(control de cambios formal), las correcciones aplicadas al documento de Definición del Proyecto
(Fase 1) tras el diseño definitivo del modelo de datos realizado en la Fase 2.

La Fase 1 fue evaluada y aprobada (nota 60/70). Durante la Fase 2, al construir el modelo de
datos relacional, se detectó que **dos frases del documento describían la arquitectura de
persistencia de una forma que no corresponde al modelo finalmente implementado**. Se corrigieron
esas frases para que la documentación sea fiel al sistema real, dejando aquí la evidencia del
antes y el después.

Las versiones conservadas en el repositorio son:
- **Versión original (entregada en Fase 1):** `...(Español)0.md`
- **Versión corregida (vigente):** `...(Español).md`

Ambas tienen la misma extensión (842 líneas); los únicos cambios son los dos que se detallan a
continuación.

---

## 2. Correcciones aplicadas

### Corrección 1 — Pertinencia con el perfil de egreso (línea 123)

**Motivo:** el modelo definitivo es íntegramente relacional y normalizado hasta 2FN. La mención
a "modelado documental" sugería una arquitectura mixta (relacional + NoSQL) que nunca se
implementó.

**Antes (original):**
> El diseño en cascada exige un modelado de datos relacional **y documental** exhaustivo en
> PostgreSQL, cubriendo la competencia de arquitectura de datos. […]

**Después (corregido):**
> El diseño en cascada exige un modelado de datos relacional **normalizado (hasta 2FN)**
> exhaustivo en PostgreSQL, cubriendo la competencia de arquitectura de datos. […]

---

### Corrección 2 — Relación con intereses profesionales (línea 132)

**Motivo:** la expresión "persistencia híbrida" implica combinar motores relacional y no
relacional. El sistema usa exclusivamente PostgreSQL (relacional), con particionamiento por
tiempo para la telemetría; esa es la descripción correcta.

**Antes (original):**
> […] el diseño de **persistencia híbrida** para la alta concurrencia clínica satisface los
> objetivos de desarrollo en Data Engineering y administración de bases de datos Cloud. […]

**Después (corregido):**
> […] el diseño de **persistencia relacional normalizada en PostgreSQL (con particionado por
> tiempo para la telemetría)** para la alta concurrencia clínica satisface los objetivos de
> desarrollo en Data Engineering y administración de bases de datos Cloud. […]

---

## 3. Alcance de las correcciones

- **Son solo dos frases.** El resto del documento de Fase 1 (objetivos, metodología, cronograma,
  Carta Gantt, plan de trabajo, equipo, roles) se mantiene **íntegro y sin cambios**, tal como
  fue aprobado.
- **No alteran el alcance ni los compromisos** del proyecto: ajustan la descripción técnica de
  la base de datos para que coincida con el modelo construido.
- Las métricas cuantitativas de los objetivos **se conservan** con orientación de análisis de
  negocio (proyección de producto a futuro), según lo acordado con el docente en Fase 1.

## 4. Trazabilidad

| Elemento | Referencia |
|---|---|
| Versión original | `docs/1.5_...(Español)0.md` |
| Versión corregida | `docs/1.5_...(Español).md` |
| Verificación del cambio | `diff` entre ambas versiones: 2 líneas modificadas (123 y 132) |
| Justificación técnica detallada | `docs/Normalizacion_2FN_AgeCare.md` |
| Declaración en el informe de avance | `docs/Guía2 Desarrollo Proyecto.md`, apartado "Objetivos (ajuste)" y "Actividades ajustadas" |

Esta corrección se declara explícitamente en el Informe de Avance de Fase 2 (Guía 2) como la
única modificación de redacción respecto del documento de Fase 1.
