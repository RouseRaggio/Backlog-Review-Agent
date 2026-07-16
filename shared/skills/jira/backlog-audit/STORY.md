# Story Audit Standard

**Skill:** Backlog Audit

**Versión:** 1.0.0

**Tipo de Issue:** Story

---

# Objetivo

Este documento define el estándar organizacional utilizado para auditar Historias de Usuario (Stories) en Jira.

Su propósito es garantizar que toda Historia de Usuario posea la información necesaria para ser comprendida, refinada, estimada, desarrollada y validada por el equipo.

---

# Objetivo de la Auditoría

Una Story será considerada lista para desarrollo únicamente cuando cumpla los criterios funcionales, de calidad y de negocio definidos en este documento.

---

# Información Obligatoria

## Identificador

Debe existir un identificador único.

Ejemplo

ABC-125

---

## Resumen

Debe existir un resumen.

Debe describir claramente el objetivo.

No debe contener abreviaturas innecesarias.

Debe ser entendible por cualquier miembro del equipo.

---

## Descripción

Toda Story debe poseer una descripción.

La descripción debe explicar claramente el contexto del requerimiento.

Debe evitar ambigüedades.

Debe permitir comprender el alcance.

---

# Formato de Historia de Usuario

Cuando aplique Scrum, la Story deberá seguir el formato:

Como <tipo de usuario>

Quiero <funcionalidad>

Para <beneficio esperado>

Ejemplo

Como cliente

Quiero consultar el historial de pedidos

Para conocer mis compras anteriores

---

# Validaciones del Formato

Verificar que exista:

- Como
- Quiero
- Para

La ausencia de cualquiera de estos elementos deberá registrarse como Hallazgo.

---

# Calidad de la Historia

La Story debe responder claramente:

- ¿Quién necesita la funcionalidad?
- ¿Qué necesita?
- ¿Por qué la necesita?
- ¿Cuál es el beneficio?

---

# Criterios de Aceptación

Toda Story deberá incluir criterios de aceptación.

Los criterios deben ser:

- Claros
- Completos
- Verificables
- Medibles
- Independientes

No deben describir la implementación.

---

# Reglas de Negocio

Cuando existan reglas de negocio deberán estar documentadas.

Ejemplos:

- Límites.
- Restricciones.
- Validaciones.
- Condiciones.
- Políticas.

---

# Requisitos Funcionales

La Story deberá describir correctamente el comportamiento esperado.

No deberá dejar funcionalidades implícitas.

---

# Requisitos No Funcionales

Cuando aplique deberán documentarse aspectos como:

- Seguridad
- Rendimiento
- Disponibilidad
- Accesibilidad
- Compatibilidad
- Escalabilidad

---

# Prioridad

Toda Story deberá tener una prioridad asignada.

La prioridad deberá corresponder al valor del negocio.

---

# Estimación

Toda Story deberá ser estimable.

Cuando la organización lo requiera deberá incluir Story Points.

---

# Epic

Toda Story deberá pertenecer a una Epic.

La ausencia de Epic deberá generar un hallazgo.

---

# Sprint

Cuando la Story pertenezca a un Sprint deberá verificarse que:

- El Sprint sea correcto.
- La Story esté preparada para desarrollo.

---

# Dependencias

Las dependencias deberán estar identificadas.

Cuando existan bloqueos deberán documentarse.

---

# Riesgos

Cuando existan riesgos deberán registrarse.

Ejemplos:

- Dependencia externa.
- Restricción técnica.
- Información pendiente.
- Integraciones.

---

# Responsable

Cuando la organización lo requiera deberá existir un responsable.

---

# Etiquetas

Las etiquetas deberán seguir el estándar organizacional.

---

# Definition of Ready (DoR)

Una Story se considera Ready cuando:

- Tiene título.
- Tiene descripción.
- Sigue el formato de Historia de Usuario.
- Posee criterios de aceptación.
- Tiene prioridad.
- Tiene estimación.
- Pertenece a una Epic.
- No presenta información ambigua.
- Puede ser comprendida por cualquier miembro del equipo.
- Puede estimarse.
- Puede desarrollarse.

---

# Hallazgos

La auditoría deberá detectar, como mínimo:

- Historia sin descripción.
- Historia incompleta.
- Historia ambigua.
- Historia sin criterios de aceptación.
- Historia sin Epic.
- Historia sin prioridad.
- Historia sin estimación.
- Historia sin reglas de negocio.
- Historia sin requisitos no funcionales cuando sean necesarios.
- Historia con información contradictoria.

---

# Recomendaciones

Cada hallazgo deberá incluir una recomendación accionable.

Ejemplo

Hallazgo

La Story no posee criterios de aceptación.

Recomendación

Agregar criterios de aceptación verificables que permitan validar el comportamiento esperado.

---

# Severidad

## Crítica

Impide iniciar el desarrollo.

Ejemplos

- Sin descripción.
- Sin criterios de aceptación.
- Historia incomprensible.

---

## Alta

Genera alto riesgo durante el desarrollo.

Ejemplos

- Sin Epic.
- Sin reglas de negocio.
- Ambigüedad importante.

---

## Media

Debe corregirse antes del Sprint.

Ejemplos

- Etiquetas incorrectas.
- Prioridad inconsistente.

---

## Baja

Representa una oportunidad de mejora.

Ejemplos

- Mejorar redacción.
- Agregar contexto.

---

# Estado Final

Al finalizar la auditoría la Story deberá clasificarse como:

- READY
- NEEDS REVIEW
- NEEDS REFINEMENT
- BLOCKED

---

# Resultado Esperado

Una Story auditada deberá:

- Ser clara.
- Ser completa.
- Ser consistente.
- Ser estimable.
- Ser verificable.
- Estar preparada para desarrollo.
- Cumplir el estándar organizacional.
