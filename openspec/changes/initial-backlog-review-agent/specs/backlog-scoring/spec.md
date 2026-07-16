## ADDED Requirements

### Requirement: Cálculo del Backlog Quality Score
El sistema SHALL calcular el Backlog Quality Score (BQS) como un valor entre 0 y 100.
El BQS SHALL ser el promedio ponderado de todas las reglas evaluadas sobre todos los issues.
El sistema SHALL calcular subtotales por regla y por issue.

#### Scenario: Cálculo de BQS básico
- **WHEN** se evalúan 10 issues con 5 reglas cada uno y todas las reglas son aprobadas
- **THEN** el BQS es 100

#### Scenario: Cálculo con reglas falladas
- **WHEN** el 50% de las evaluaciones de reglas son falladas
- **THEN** el BQS es 50

### Requirement: Desglose de puntuación
El sistema SHALL desglosar la puntuación por regla (promedio entre todos los issues).
El sistema SHALL desglosar la puntuación por issue (promedio de todas las reglas aplicadas).

#### Scenario: Puntuación por regla
- **WHEN** se evalúan 10 issues y la regla "descripción" falla en 3
- **THEN** la puntuación de la regla "descripción" es 70

#### Scenario: Puntuación por issue
- **WHEN** un issue falla 2 de 5 reglas
- **THEN** la puntuación del issue es 60

### Requirement: Umbrales de calidad
El sistema SHALL permitir configurar umbrales de calidad (ej: verde > 80, amarillo 50-80, rojo < 50).
El sistema SHALL clasificar el backlog según el BQS en las categorías configuradas.

#### Scenario: Clasificación por umbrales
- **WHEN** el BQS es 85
- **THEN** el backlog se clasifica como "bueno" (verde)
