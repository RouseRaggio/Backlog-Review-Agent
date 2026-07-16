# Backlog Quality Score

**Skill:** Backlog Audit

**Versión:** 1.0.0

---

# Objetivo

Definir el método para calcular el Backlog Quality Score (BQS), un indicador que representa el nivel de calidad de un Issue o de un Backlog completo.

El puntaje tendrá un rango de **0 a 100**, donde 100 representa un backlog completamente listo para desarrollo.

---

# Escala de Calidad

| Puntaje | Estado | Interpretación |
|----------|---------|----------------|
| 90 - 100 | READY | El Issue cumple los estándares organizacionales. |
| 75 - 89 | NEEDS REVIEW | Existen observaciones menores. |
| 50 - 74 | NEEDS REFINEMENT | Requiere refinamiento antes de estimarse. |
| 0 - 49 | BLOCKED | No debe pasar a desarrollo. |

---

# Criterios de Evaluación

| Categoría | Peso |
|-----------|------|
| Información General | 10% |
| Calidad de la Descripción | 15% |
| Historia de Usuario / Contexto | 15% |
| Criterios de Aceptación | 20% |
| Reglas de Negocio | 10% |
| Priorización | 5% |
| Estimación | 10% |
| Asociación con Epic | 5% |
| Riesgos y Dependencias | 5% |
| Aspectos No Funcionales | 5% |

---

# Penalizaciones

## Crítica

-20 puntos

Ejemplos:

- Sin descripción.
- Sin criterios de aceptación.
- Historia imposible de entender.

---

## Alta

-10 puntos

Ejemplos:

- Sin Epic.
- Sin reglas de negocio.

---

## Media

-5 puntos

Ejemplos:

- Sin prioridad.
- Sin estimación.

---

## Baja

-2 puntos

Ejemplos:

- Errores de redacción.
- Falta de etiquetas.

---

# Resultado

Al finalizar la auditoría el sistema deberá generar:

- Puntaje final.
- Estado.
- Número de hallazgos.
- Hallazgos críticos.
- Recomendaciones.