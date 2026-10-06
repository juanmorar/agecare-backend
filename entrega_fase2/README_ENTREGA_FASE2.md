# Entrega Avance Fase 2 — AgeCare (Grupo 1)

**Capstone APT122 · DUOC UC · Sección 003D**
**Equipo:** Javier Cerna Chávez · Benjamín Camus · Juan Mora
**Fecha límite de entrega:** martes 6 de octubre, 23:59 hrs
**Repositorio de entrega DUOC:** https://github.com/Jaacern/G1_CAPSTONE_003D
**Repositorio técnico (código y BD):** https://github.com/juanmorar/agecare-backend
**API desplegada (evidencia en vivo):** https://agecare-api.javiercerna.dev/docs

---

## 1. Qué es esta carpeta

Esta carpeta `entrega_fase2/` contiene **todos los documentos listos** para subir al repositorio
de entrega DUOC (`G1_CAPSTONE_003D`), ya organizados en la estructura exacta que exige el correo
de la asignatura. Basta copiar el contenido de cada subcarpeta a su carpeta correspondiente en
el repositorio de entrega.

El enfoque del proyecto es **Tradicional (relacional)**, por lo que las evidencias de proyecto
corresponden a: Documento de Requerimientos Funcionales, Modelo Relacional en español y
Diccionario de Datos.

---

## 2. Estructura de la entrega (según el correo)

El correo indica subir, dentro de la carpeta `Fase 2/` del repositorio DUOC:

```
Fase 2/
├── Evidencias Individuales/   ← evidencia 2.2 de cada integrante
├── Evidencias Grupales/       ← evidencia 2.4 + planilla de evaluación
└── Evidencias Proyecto/       ← requerimientos, modelo relacional y diccionario de datos
```

---

## 3. Mapa de archivos: qué va en cada carpeta

### 📁 Evidencias Grupales

| Archivo en esta carpeta | Corresponde a |
|---|---|
| `2.4_GuiaEstudiante_Fase2_DesarrolloProyecto_APT.md` | Evidencia **2.4** — Informe de avance (Guía 2). Documento completado por el equipo. |
| `PLANILLA_DE_EVALUACION_AVANCE_FASE2.md` | Planilla de evaluación del avance (rúbrica de 8 indicadores). |

### 📁 Evidencias Individuales

| Archivo en esta carpeta | Corresponde a |
|---|---|
| `2.2_APT122_AutoevaluacionAvance_Fase2_PLANTILLA.md` | Evidencia **2.2** — Autoevaluación. **PLANTILLA**: cada integrante debe generar su propia copia nombrada `Apellido_Nombre_2.2_APT122_AutoevaluacionAvance_Fase2`. Son **3 archivos** (Cerna_Javier, Camus_Benjamín, Mora_Juan). |

> ⚠️ **Pendiente del equipo:** las tres autoevaluaciones individuales las completa cada
> integrante por separado (es evidencia personal). Esta carpeta solo deja la plantilla base.

### 📁 Evidencias Proyecto (enfoque Tradicional / relacional)

| Archivo en esta carpeta | Corresponde a |
|---|---|
| `00_ERS_Simplificado_Fase1.md` | ERS de Fase 1 (fuente de los requisitos). Contexto. |
| `01_Documento_Requerimientos_Funcionales.md` | **Documento de Requerimientos Funcionales** (RF-01…82, RNF-01…25). *Exigido por el correo.* |
| `02_Modelo_Relacional_Definitivo.md` | **Modelo Relacional en español** (24 tablas, bloques, matriz de cobertura). *Exigido por el correo.* |
| `03_Diccionario_de_Datos.md` | **Diccionario de Datos** en español (columna por columna). *Exigido por el correo.* |
| `04_Diagrama_ER.dbml` | Diagrama Entidad-Relación para dbdiagram.io (exportable a PNG/PDF). |
| `04_Diagrama_ER_Mermaid.md` | Diagrama ER que se renderiza directo en GitHub. |
| `05_Normalizacion_2FN.md` | Documento de normalización hasta 2FN (respaldo de calidad del diseño). |
| `06_Analisis_de_Realidad_y_Decisiones.md` | Análisis de realidad y decisiones de ingeniería (robustez del modelo). |
| `07_schema_completo.sql` | Script SQL ejecutable del modelo completo (implementación verificable). |
| `09_Historias_de_Usuario.md` | Historias de usuario trazadas a RF y casos de uso (complemento). |

---

## 4. Checklist antes de subir

- [ ] Copiar las 3 subcarpetas a `Fase 2/` en `G1_CAPSTONE_003D`.
- [ ] Cada integrante genera y sube su **autoevaluación 2.2 individual** (3 archivos).
- [ ] **Benjamín Camus** sube sus commits de arquitectura de datos al repositorio técnico, para
      evidenciar la participación equitativa de los 3 integrantes (indicador 7 de la rúbrica).
- [ ] Verificar que el enlace a la API (`agecare-api.javiercerna.dev`) esté activo durante la
      evaluación como evidencia en vivo.
- [ ] (Opcional) Exportar el diagrama ER a PNG desde dbdiagram.io para incluirlo como imagen.

---

## 5. Relación con la Fase 1 (congruencia)

- Las evidencias de proyecto se construyen sobre el **ERS aprobado en Fase 1** (misma
  numeración RF/RNF).
- El informe de avance (2.4) mantiene **objetivos y metodología sin cambios**, declarando la
  única corrección de redacción (persistencia de datos), documentada en
  `docs/CHANGELOG_Correcciones_Fase1.md` del repositorio técnico.
- El cronograma y la metodología en cascada se respetan tal como fueron definidos en Fase 1.
