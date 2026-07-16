## 1. Setup del proyecto

- [ ] 1.1 Crear estructura de directorios `apps/backlog-review-agent/` con capas: entities, use_cases, interface_adapters, frameworks
- [ ] 1.2 Crear archivo `pyproject.toml` con dependencias: atlassian-python-api, httpx, jinja2, pydantic, pyyaml
- [ ] 1.3 Configurar pytest, mypy y ruff en pyproject.toml
- [ ] 1.4 Verificar que la estructura del proyecto y las herramientas base funcionan correctamente

## 2. Configuración

- [ ] 2.1 Definir modelo `AppConfig` con validación Pydantic para toda la configuración de la aplicación
- [ ] 2.2 Implementar `ConfigLoader` para cargar y validar configuración desde archivo YAML
- [ ] 2.3 Implementar soporte de variables de entorno como override de valores en config.yaml
- [ ] 2.4 Crear archivo `config.yaml` de ejemplo con todos los valores documentados
- [ ] 2.5 Implementar excepciones personalizadas: `ConfigError`, `JiraConnectionError`, `JiraAuthError`, `JiraRateLimitError`, `RuleValidationError`
- [ ] 2.6 Escribir pruebas unitarias para `AppConfig`, `ConfigLoader`, variables de entorno y excepciones personalizadas

## 3. Entidades de dominio (Domain Entities)

- [ ] 3.1 Implementar entidad `Issue` con todos los campos requeridos (key, summary, description, status, priority, issue_type, assignee, labels, created, updated, story_points)
- [ ] 3.2 Implementar entidad `Project` con campos requeridos (key, name, lead, category)
- [ ] 3.3 Implementar entidad `QualityRule` con nombre, descripción, peso y función de evaluación
- [ ] 3.4 Implementar entidad `QualityRuleResult` con estado (pass/fail/warning), mensaje y peso asociado
- [ ] 3.5 Implementar entidad `QualityReport` con BQS global, resultados por issue, resultados por regla y metadatos
- [ ] 3.6 Implementar objetos valor: `BacklogQualityScore`, `Threshold`, `Severity` con validación Pydantic
- [ ] 3.7 Escribir pruebas unitarias para todas las entidades y objetos valor

## 4. Interfaces de repositorio (Repository Interfaces)

- [ ] 4.1 Definir interfaz `IssueRepository` (ABC/protocol) con métodos `fetch_by_jql` y `get_by_key`
- [ ] 4.2 Definir interfaz `RuleRepository` (ABC/protocol) con métodos `load_all` y `get_by_name`
- [ ] 4.3 Escribir pruebas unitarias con mocks para ambas interfaces

## 5. Infraestructura (Infrastructure)

- [ ] 5.1 Implementar `JiraApiClient` como wrapper de atlassian-python-api con autenticación básica y por token
- [ ] 5.2 Implementar mapeo de respuesta JSON de Jira a modelo `Issue` con validación de campos obligatorios
- [ ] 5.3 Implementar `JiraIssueRepository` que implementa `IssueRepository` con fetch_by_jql y get_by_key
- [ ] 5.4 Implementar paginación en `JiraIssueRepository` (parámetros max_results, start_at y paginación automática)
- [ ] 5.5 Implementar políticas de reintento con backoff exponencial para errores 429, 5xx y timeouts de red
- [ ] 5.6 Implementar sistema de logging estructurado (`logger.py`) con formato JSON, niveles configurables y salida a archivo
- [ ] 5.7 Implementar `YamlRuleRepository` que implementa `RuleRepository` cargando y validando reglas desde YAML
- [ ] 5.8 Escribir pruebas unitarias para `JiraApiClient` (autenticación, errores, reintentos)
- [ ] 5.9 Escribir pruebas unitarias para `JiraIssueRepository` (paginación, mapeo, casos borde)
- [ ] 5.10 Escribir pruebas unitarias para `YamlRuleRepository` (carga, validación, errores de formato)
- [ ] 5.11 Escribir pruebas unitarias para el sistema de logging

## 6. Motor de reglas de calidad (Rule Engine)

- [ ] 6.1 Implementar `QualityRuleEvaluator` que ejecuta reglas sobre un issue y produce `QualityRuleResult`
- [ ] 6.2 Implementar `RuleRegistry` como contenedor singleton de reglas registradas con registro y consulta por nombre
- [ ] 6.3 Implementar reglas predefinidas: descripción no vacía, criterios de aceptación presentes, prioridad definida, tipo definido, estimación presente, asignado presente, labels relevantes
- [ ] 6.4 Implementar `BacklogScoringService` para cálculo de BQS con ponderación de reglas y desglose por proyecto/tipo/prioridad
- [ ] 6.5 Escribir pruebas unitarias para `QualityRuleEvaluator` y `RuleRegistry`
- [ ] 6.6 Escribir pruebas unitarias para todas las reglas predefinidas
- [ ] 6.7 Escribir pruebas unitarias para `BacklogScoringService`

## 7. Casos de uso (Use Cases)

- [ ] 7.1 Implementar `FetchIssuesUseCase` que orquesta conexión JQL, paginación y mapeo a entidades de dominio
- [ ] 7.2 Implementar `EvaluateQualityUseCase` que aplica el evaluador de reglas a todos los issues obtenidos
- [ ] 7.3 Implementar `BacklogScoringUseCase` que calcula BQS y desgloses a partir de resultados de evaluación
- [ ] 7.4 Implementar `GenerateReportUseCase` que orquesta la generación del reporte a través del presentador
- [ ] 7.5 Escribir pruebas unitarias para todos los casos de uso con inyección de dependencias mock

## 8. Presentadores (Presenters)

- [ ] 8.1 Crear template HTML base con Jinja2 (resumen ejecutivo, tabla de issues, desglose de reglas, métricas globales)
- [ ] 8.2 Implementar `HtmlReportPresenter` que transforma `QualityReport` a HTML usando el template
- [ ] 8.3 Implementar estilos CSS embebidos para reporte responsivo con diseño profesional
- [ ] 8.4 Implementar indicadores visuales de color por umbral (verde/amarillo/rojo) con tooltips informativos
- [ ] 8.5 Escribir pruebas unitarias para `HtmlReportPresenter` (renderizado, datos vacíos, casos borde)

## 9. CLI y composición (CLI & Composition Root)

- [ ] 9.1 Implementar composición raíz en `app.py` con inyección de dependencias que ensambla todas las capas
- [ ] 9.2 Implementar `CliController` que orquesta el flujo completo (conectar → evaluar → reportar)
- [ ] 9.3 Implementar configuración de logging desde CLI (--verbose, --log-file, --quiet)
- [ ] 9.4 Implementar punto de entrada `main.py` con argumentos CLI usando argparse (--config, --jql, --output, --verbose)
- [ ] 9.5 Escribir pruebas unitarias para `CliController` y parseo de argumentos CLI

## 10. Pruebas de integración (Integration Tests)

- [ ] 10.1 Implementar prueba de integración: `ConfigLoader` → `JiraIssueRepository` → obtención y mapeo de issues
- [ ] 10.2 Implementar prueba de integración: `RuleRegistry` → `QualityRuleEvaluator` → `BacklogScoringService`
- [ ] 10.3 Implementar prueba de integración: `EvaluateQualityUseCase` → `GenerateReportUseCase` → `HtmlReportPresenter`
- [ ] 10.4 Implementar prueba end-to-end del flujo completo usando un proyecto Jira de prueba o mock HTTP
- [ ] 10.5 Implementar prueba de compatibilidad de modelos y validación cruzada de esquemas

## 11. Aseguramiento de calidad (Quality Assurance)

- [ ] 11.1 Ejecutar ruff sobre todo el proyecto y corregir todos los errores de estilo y formato
- [ ] 11.2 Ejecutar mypy en modo estricto sobre todo el proyecto y corregir todos los errores de tipos
- [ ] 11.3 Ejecutar pytest con cobertura y verificar que la cobertura supera el 80%
- [ ] 11.4 Configurar validación CI (GitHub Actions) con jobs para ruff, mypy y pytest en cada push y PR

## 12. Documentación (Documentation)

- [ ] 12.1 Crear `README.md` con descripción del proyecto, requisitos, instalación, configuración y ejemplos de uso
- [ ] 12.2 Crear guía de configuración detallada con ejemplos de `config.yaml` y variables de entorno disponibles
- [ ] 12.3 Crear diagramas de arquitectura mostrando las capas de Clean Architecture y el flujo de datos entre ellas
- [ ] 12.4 Validar el change contra OpenSpec: verificar que todos los artefactos (specs, tareas, diseño) están completos y coherentes
