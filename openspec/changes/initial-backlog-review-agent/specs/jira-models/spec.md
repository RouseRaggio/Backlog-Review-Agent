## ADDED Requirements

### Requirement: Modelo Issue
El sistema SHALL definir un modelo Issue con los campos: id, key, summary, description, issue_type, priority, status, assignee, labels, created, updated, due_date, acceptance_criteria, estimation, project, components, fix_versions.
El modelo Issue SHALL ser una entidad de dominio Pydantic sin dependencias de infraestructura.

#### Scenario: Creación de Issue válido
- **WHEN** se crea un Issue con todos los campos requeridos
- **THEN** el modelo valida y retorna una instancia de Issue

#### Scenario: Issue con campos faltantes
- **WHEN** se crea un Issue sin campos requeridos
- **THEN** el modelo lanza un error de validación

### Requirement: Modelo QualityRule
El sistema SHALL definir un modelo QualityRule con: nombre, descripción, peso, función de evaluación.
El sistema SHALL definir un modelo QualityReport con: BQS general, resultados por regla, resultados por issue, fecha de evaluación, metadatos de la consulta.

#### Scenario: Creación de QualityReport
- **WHEN** se completa la evaluación de un backlog
- **THEN** se crea un QualityReport con todos los resultados agregados

### Requirement: Modelo Project
El sistema SHALL definir un modelo Project con: id, key, name, description, lead, category.

#### Scenario: Creación de Project
- **WHEN** se mapea un proyecto de Jira
- **THEN** el modelo Project contiene todos los campos relevantes
