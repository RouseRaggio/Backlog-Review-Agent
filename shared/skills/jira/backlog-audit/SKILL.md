# Skill: Backlog Audit

**Versión:** 1.0.0

**Categoría:** Jira / Quality Assurance

**Plataforma:** AI-QA-Agents

**Estado:** Draft

---

# Objetivo

La Skill **Backlog Audit** proporciona el conocimiento necesario para realizar una auditoría funcional de un Backlog de Jira utilizando estándares de calidad organizacionales.

Su propósito es determinar si un Backlog se encuentra preparado para iniciar el proceso de desarrollo, identificando inconsistencias, riesgos, información faltante y oportunidades de mejora.

Esta Skill encapsula el conocimiento utilizado por los equipos de QA durante las revisiones de Backlog y Sprint Planning.

---

# Responsabilidad

Esta Skill es responsable de:

- Analizar elementos del Backlog.
- Aplicar reglas de auditoría.
- Detectar incumplimientos.
- Identificar riesgos.
- Generar observaciones.
- Generar recomendaciones.
- Calcular un indicador de calidad del Backlog.

Esta Skill **NO** modifica información en Jira.

---

# Cuándo utilizar esta Skill

Utilizar esta Skill cuando sea necesario:

- Auditar un Product Backlog.
- Auditar un Sprint Activo.
- Auditar un Sprint específico.
- Auditar una Epic.
- Auditar un conjunto de Issues.
- Validar la calidad de un Backlog antes del Sprint Planning.
- Detectar historias incompletas.
- Verificar el cumplimiento de estándares organizacionales.

---

# Cuándo NO utilizar esta Skill

No utilizar esta Skill para:

- Modificar Issues.
- Crear Historias.
- Crear Bugs.
- Estimar Story Points.
- Cambiar Prioridades.
- Actualizar Jira.

Para esas actividades deberán utilizarse otras Skills.

---

# Entradas

La Skill requiere como entrada:

- Proyecto Jira.
- Sprint (opcional).
- Epic (opcional).
- Lista de Issues (opcional).
- Configuración de reglas organizacionales.

---

# Salidas

La Skill debe generar:

- Hallazgos.
- Observaciones.
- Recomendaciones.
- Estado de Auditoría.
- Backlog Quality Score.
- Reporte Ejecutivo.

---

# Tipos de Issue soportados

La Skill deberá soportar como mínimo:

- Epic
- Story
- Task
- Bug
- Sub-task

La implementación deberá permitir extender fácilmente el soporte a nuevos tipos de Issue.

---

# Criterios de Auditoría

La Skill deberá evaluar como mínimo:

- Estructura General
- Calidad de la Descripción
- Historia de Usuario
- Criterios de Aceptación
- Priorización
- Estimación
- Aspectos Funcionales
- Aspectos No Funcionales
- Asociación con Epic
- Riesgos
- Dependencias
- Estado Final

---

# Flujo General

La Skill deberá seguir el siguiente procedimiento:

1. Obtener los elementos del Backlog.

2. Clasificar los Issues por tipo.

3. Seleccionar las reglas correspondientes.

4. Auditar cada Issue.

5. Registrar Hallazgos.

6. Generar Recomendaciones.

7. Calcular el Backlog Quality Score.

8. Clasificar el Estado Final.

9. Generar el Reporte Ejecutivo.

---

# Estados de Auditoría

Cada Issue deberá finalizar con uno de los siguientes estados.

## READY

Cumple todos los criterios obligatorios.

Puede pasar al proceso de desarrollo.

---

## NEEDS REVIEW

Presenta observaciones menores.

Debe revisarse antes del Sprint Planning.

---

## NEEDS REFINEMENT

Presenta información insuficiente.

Debe refinarse antes de ser estimado.

---

## BLOCKED

No puede desarrollarse.

Presenta incumplimientos críticos.

---

# Severidad

Los hallazgos deberán clasificarse como:

## Crítica

Impide iniciar el desarrollo.

---

## Alta

Genera alto riesgo durante el desarrollo.

---

## Media

Debe corregirse antes del Sprint.

---

## Baja

Representa una oportunidad de mejora.

---

# Reglas Generales

Toda auditoría deberá:

- Ser objetiva.
- Basarse en reglas organizacionales.
- Evitar juicios subjetivos.
- Explicar el motivo del hallazgo.
- Generar una recomendación accionable.

---

# Calidad de la Skill

Toda auditoría deberá cumplir los siguientes principios:

- Consistencia.
- Repetibilidad.
- Trazabilidad.
- Configurabilidad.
- Transparencia.

---

# Dependencias

Esta Skill utiliza conocimiento definido en:

- STORY.md
- TASK.md
- BUG.md
- EPIC.md
- SUBTASK.md
- SCORING.md
- CHECKLIST.md
- BEST_PRACTICES.md

---

# Restricciones

La Skill:

- No modifica Jira.
- No crea Issues.
- No elimina información.
- No actualiza estados.
- No cambia prioridades.

Su responsabilidad es exclusivamente analizar y generar recomendaciones.

---

# Resultado Esperado

Al finalizar la ejecución, el usuario deberá conocer:

- El estado general del Backlog.
- Los Issues con problemas.
- Las observaciones encontradas.
- Las recomendaciones.
- Los riesgos identificados.
- El Backlog Quality Score.
- Los elementos que requieren refinamiento antes del desarrollo.

---

# Filosofía

Esta Skill no busca reemplazar al Product Owner ni al equipo de QA.

Su propósito es automatizar tareas repetitivas de auditoría, permitiendo que los especialistas concentren su esfuerzo en el análisis funcional y la toma de decisiones.