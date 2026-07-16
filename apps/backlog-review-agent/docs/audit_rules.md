# Backlog Review Agent - Audit Rules

## Introducción

Este documento define las reglas de auditoría que el Backlog Review Agent utilizará para evaluar la calidad del Product Backlog en Jira.

Las reglas están basadas en el estándar de calidad utilizado por la empresa para la construcción y mantenimiento de Backlogs.

Cada regla se clasifica en:

- **Automática:** puede evaluarse mediante código.
- **IA:** requiere análisis semántico mediante un modelo de lenguaje.

---

# BR-001 - El Issue debe tener un título

**Aplica a**

- Epic
- Historia
- Tarea
- Bug
- Subtarea

**Tipo**

Automática

**Validación**

El campo Summary no debe estar vacío.

**Resultado**

PASS

El Issue posee un título.

FAIL

El Issue no tiene título.

---

# BR-002 - El Issue debe tener descripción

**Aplica a**

- Epic
- Historia
- Tarea
- Bug

**Tipo**

Automática

**Validación**

El campo Description debe existir.

---

# BR-003 - El Issue debe tener prioridad

**Aplica a**

Todos los Issues.

**Tipo**

Automática

**Validación**

Priority debe existir.

---

# BR-004 - El Issue debe tener responsable

**Aplica a**

Historia

Tarea

Bug

Subtarea

**Tipo**

Automática

**Validación**

Debe existir un Assignee.

---

# BR-005 - El Issue debe pertenecer a un Sprint cuando corresponda

**Aplica a**

Historia

Tarea

Bug

Subtarea

**Tipo**

Automática

**Validación**

Debe estar asociado a un Sprint activo cuando el Issue haga parte del Sprint Planning.

---

# BR-006 - El Issue debe estar asociado a una Epic

**Aplica a**

Historia

Tarea

Bug

**Tipo**

Automática

**Validación**

Debe existir una Epic relacionada.

---

# BR-007 - Las Historias deben tener Story Points

**Aplica a**

Historia

**Tipo**

Automática

**Validación**

Story Points debe ser mayor que cero.

---

# BR-008 - La Historia debe tener criterios de aceptación

**Aplica a**

Historia

**Tipo**

Automática

**Validación**

Acceptance Criteria no debe estar vacío.

---

# BR-009 - El Bug debe contener información suficiente

**Aplica a**

Bug

**Tipo**

IA

**Validación**

El agente debe determinar si el Bug contiene información suficiente para ser reproducido.

Debe evaluar:

- contexto
- pasos
- resultado esperado
- resultado obtenido

---

# BR-010 - La Historia debe seguir el estándar organizacional

**Aplica a**

Historia

**Tipo**

IA

**Validación**

La Historia debe seguir la estructura:

Como...

Quiero...

Para...

---

# BR-011 - La descripción debe ser clara

**Aplica a**

Historia

Tarea

Bug

Epic

**Tipo**

IA

**Validación**

El agente evaluará:

- claridad
- ambigüedad
- completitud
- coherencia

---

# BR-012 - Los criterios de aceptación deben ser verificables

**Aplica a**

Historia

**Tipo**

IA

**Validación**

Cada criterio debe ser:

- claro
- medible
- verificable
- independiente

---

# BR-013 - La Historia debe ser estimable

**Aplica a**

Historia

**Tipo**

IA

**Validación**

El agente debe determinar si la información existente permite realizar una estimación razonable.

---

# BR-014 - La Historia debe contener reglas de negocio

**Aplica a**

Historia

**Tipo**

IA

**Validación**

El agente evaluará si existen reglas de negocio suficientes para comprender el comportamiento esperado.

---

# BR-015 - La Historia debe definir aspectos funcionales

**Aplica a**

Historia

**Tipo**

IA

**Validación**

Debe existir información suficiente para comprender la funcionalidad solicitada.

---

# BR-016 - La Historia debe definir aspectos no funcionales

**Aplica a**

Historia

**Tipo**

IA

**Validación**

Cuando aplique, deben especificarse requisitos como:

- rendimiento
- seguridad
- accesibilidad
- compatibilidad

---

# BR-017 - La Historia no debe presentar ambigüedades

**Aplica a**

Historia

**Tipo**

IA

**Validación**

El agente debe identificar términos ambiguos como:

- rápido
- fácil
- adecuado
- eficiente
- algunos
- varios
- etc.

---

# BR-018 - La Historia debe ser consistente

**Aplica a**

Historia

**Tipo**

IA

**Validación**

No debe contener contradicciones entre:

- descripción
- criterios
- reglas de negocio

---

# BR-019 - El lenguaje debe ser profesional

**Aplica a**

Todos los Issues.

**Tipo**

IA

**Validación**

El lenguaje utilizado debe ser:

- claro
- técnico
- objetivo

---

# BR-020 - Generación del Backlog Quality Score

**Aplica a**

Backlog completo.

**Tipo**

Automática

**Resultado**

El agente calculará un indicador global de calidad considerando el cumplimiento de todas las reglas anteriores.

---

# Clasificación de Hallazgos

Cada hallazgo tendrá uno de los siguientes estados.

## PASS

Cumple completamente.

---

## WARNING

Existe una observación que debería corregirse.

---

## FAIL

No cumple el estándar.

---

## BLOCKED

El Issue no puede ingresar al Sprint hasta ser corregido.

---

# Severidad

Cada hallazgo tendrá un nivel de severidad.

- Baja
- Media
- Alta
- Crítica

---

# Resultado Final

Cada Issue recibirá un estado final.

- READY
- NEEDS REVIEW
- BLOCKED

---

# Backlog Quality Score

El Backlog Quality Score se calculará considerando el porcentaje de cumplimiento de todas las reglas aplicables.

Escala sugerida:

| Score | Estado |
|--------|--------|
| 95 - 100 | Excelente |
| 85 - 94 | Bueno |
| 70 - 84 | Requiere mejoras |
| 50 - 69 | Deficiente |
| 0 - 49 | Crítico |
