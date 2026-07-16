## Por qué

Los backlogs de Jira suelen acumular issues con información incompleta, criterios de aceptación ausentes y prioridades inconsistentes, lo que dificulta la planificación y reduce la productividad del equipo. Este agente automatiza la evaluación de calidad del backlog, proporcionando métricas objetivas y reportes que permiten a los equipos identificar y corregir problemas de forma temprana.

## Qué Cambia

- Nuevo agente `backlog-review-agent` en `apps/` que evalúa la calidad de backlogs de Jira
- Conexión a Jira Cloud mediante API REST para recuperar issues vía JQL
- Motor de reglas de calidad configurables para evaluar issues
- Cálculo del Backlog Quality Score (BQS) como métrica unificada
- Generación de reportes HTML con resultados detallados
- Modelos internos con Clean Architecture (Entities, Use Cases, Interfaces)
- Pruebas unitarias con pytest para cada capa

## Capacidades

### Nuevas Capacidades

- `jira-connection`: Conexión y autenticación con Jira Cloud via API REST, ejecución de consultas JQL y recuperación de issues
- `quality-rules`: Motor de reglas de calidad configurables para evaluar issues individuales (descripción, criterios de aceptación, prioridad, estimación, etc.)
- `backlog-scoring`: Cálculo del Backlog Quality Score (BQS) a partir de los resultados de las reglas de calidad aplicadas a un conjunto de issues
- `html-report`: Generación de reportes HTML con los resultados del análisis, incluyendo puntuaciones, reglas falladas y recomendaciones
- `jira-models`: Modelos de dominio para representar issues de Jira, proyectos, usuarios y metadatos siguiendo Clean Architecture

### Capacidades Modificadas

Ninguna. Es la primera versión del proyecto.

## Impacto

- Nuevo directorio `apps/backlog-review-agent/` con la estructura completa del agente
- Dependencias nuevas: `atlassian-python-api`, `httpx`, `jinja2`, `pydantic`
- Integración con Jira Cloud API REST
- Generación de reportes HTML autocontenidos
- Sin impacto en sistemas existentes (proyecto nuevo)
