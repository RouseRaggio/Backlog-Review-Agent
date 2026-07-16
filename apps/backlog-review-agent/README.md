# Backlog Review Agent

## Descripción

Backlog Review Agent es un agente de Inteligencia Artificial diseñado para automatizar la revisión y auditoría de historias de usuario almacenadas en Jira.

Su objetivo es mejorar la calidad del backlog antes de que las historias entren al proceso de desarrollo, detectando problemas de definición, inconsistencias, riesgos y oportunidades de mejora.

El agente forma parte de la plataforma **AI-QA-Agents**, cuyo propósito es automatizar procesos de Quality Assurance mediante agentes especializados.

---

# Objetivos

- Auditar automáticamente historias de usuario en Jira.
- Validar la calidad del backlog.
- Detectar historias incompletas o ambiguas.
- Reducir retrabajo durante el desarrollo.
- Mejorar la calidad de los requerimientos.
- Apoyar al Product Owner y al equipo de QA durante el refinamiento del backlog.

---

# Alcance

El agente analizará información proveniente de Jira como:

- Historias de Usuario
- Épicas
- Tareas
- Bugs (opcional)
- Criterios de aceptación
- Prioridades
- Etiquetas
- Componentes
- Sprint
- Versiones
- Dependencias

---

# Funcionalidades

## Validación INVEST

El agente evaluará cada historia utilizando el modelo INVEST.

- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable

---

## Revisión de criterios de aceptación

Detectará:

- criterios faltantes
- criterios ambiguos
- reglas de negocio incompletas
- casos negativos ausentes
- criterios duplicados

---

## Auditoría del backlog

Analizará:

- descripción
- objetivo
- reglas de negocio
- dependencias
- consistencia
- claridad
- completitud

---

## Detección de riesgos

Identificará riesgos como:

- historias demasiado grandes
- historias ambiguas
- dependencias ocultas
- falta de información
- inconsistencias funcionales

---

## Recomendaciones

El agente generará recomendaciones para mejorar la historia.

Ejemplo:

- Dividir la historia.
- Agregar criterios de aceptación.
- Especificar reglas de negocio.
- Eliminar ambigüedad.
- Definir casos negativos.

---

## Reportes

El agente podrá generar reportes en:

- Markdown
- HTML
- PDF
- JSON

---

# Arquitectura

El proyecto sigue los principios de:

- Clean Architecture
- SOLID
- Specification Driven Development (SDD)

La estructura principal es:

```
src/
├── domain/
├── use_cases/
├── infrastructure/
└── presentation/
```

---

# Flujo de funcionamiento

```text
Jira

↓

Obtención de historias

↓

Análisis con IA

↓

Validación INVEST

↓

Validación de criterios de aceptación

↓

Análisis de riesgos

↓

Generación de recomendaciones

↓

Reporte
```

---

# Tecnologías

- Python
- FastAPI
- Ollama
- Qwen 2.5 Coder
- Jira REST API
- Docker

---

# Estado del proyecto

Actualmente el proyecto se encuentra en desarrollo siguiendo la metodología Specification-Driven Development (SDD).

El orden de desarrollo es:

1. SRS
2. SDD
3. Implementación
4. Pruebas
5. Despliegue

---

# Estructura del proyecto

```
backlog-review-agent/

├── config/
├── docs/
├── prompts/
├── src/
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# Casos de uso principales

- Auditoría automática de historias de usuario.
- Validación de calidad del backlog.
- Apoyo al Product Owner.
- Apoyo al equipo QA.
- Preparación del Sprint Planning.
- Revisión previa al refinamiento del backlog.

---

# Futuras funcionalidades

- Integración con Confluence.
- Generación automática de historias mejoradas.
- Detección de historias duplicadas.
- Análisis de épicas completas.
- Métricas de calidad del backlog.
- Dashboard de indicadores.
- Integración con Microsoft Teams y Slack.

---

# Licencia

Uso interno de la empresa.

Todos los derechos reservados.