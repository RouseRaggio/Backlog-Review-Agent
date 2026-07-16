## ADDED Requirements

### Requirement: Definición de reglas de calidad
El sistema SHALL permitir definir reglas de calidad en un archivo de configuración YAML.
Cada regla SHALL tener: nombre, descripción, peso, función de evaluación y mensaje de error.
El sistema SHALL soportar reglas predefinidas para: descripción completa, criterios de aceptación, prioridad asignada, estimación presente, tipo de issue válido, asignado presente, labels presentes.

#### Scenario: Carga de reglas desde YAML
- **WHEN** se proporciona un archivo YAML con reglas de calidad válidas
- **THEN** el sistema carga y valida todas las reglas correctamente

#### Scenario: Regla con peso inválido
- **WHEN** una regla tiene un peso fuera del rango 0-100
- **THEN** el sistema lanza un error de validación indicando la regla y el valor inválido

### Requirement: Evaluación de reglas individuales
Cada regla SHALL evaluar un issue y retornar un resultado (aprobado/fallado) con un mensaje.
Cada regla SHALL tener un peso configurable que determina su impacto en la puntuación final.

#### Scenario: Regla aprobada
- **WHEN** un issue cumple con la condición de la regla
- **THEN** la regla retorna estado "aprobado" sin mensaje de error

#### Scenario: Regla fallada
- **WHEN** un issue no cumple con la condición de la regla
- **THEN** la regla retorna estado "fallado" con un mensaje descriptivo del problema

### Requirement: Reglas de calidad predefinidas
El sistema SHALL incluir reglas predefinidas para evaluar:
- Descripción del issue no vacía
- Criterios de aceptación presentes
- Prioridad asignada
- Tipo de issue válido
- Estimación presente (para issues de tipo Story/Task)
- Asignado presente
- Labels presentes

#### Scenario: Evaluación de descripción vacía
- **WHEN** un issue no tiene descripción
- **THEN** la regla "descripción no vacía" retorna fallado

#### Scenario: Evaluación de prioridad asignada
- **WHEN** un issue no tiene prioridad asignada
- **THEN** la regla "prioridad asignada" retorna fallado
