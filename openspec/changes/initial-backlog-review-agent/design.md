## Contexto

Los equipos de desarrollo que utilizan Jira como herramienta de gestión de proyectos enfrentan un problema recurrente: los backlogs se deterioran con el tiempo. Los issues acumulan descripciones incompletas, prioridades sin asignar, criterios de aceptación ausentes y estimaciones faltantes. Este deterioro progresivo dificulta la planificación de sprints, reduce la precisión de las estimaciones y genera incertidumbre en la toma de decisiones.

El Backlog Review Agent aborda este problema automatizando la evaluación de calidad de los backlogs de Jira Cloud. Proporciona métricas objetivas y repetibles que permiten a los equipos identificar áreas de mejora, mantener la higiene del backlog y tomar decisiones informadas basadas en datos.

El flujo de ejecución completo es:

```
+----------+     +----------+     +-----------+     +------------+     +-----------+
|  Jira    |     |  JQL     |     |  Issue    |     |  Quality   |     |  HTML     |
|  Cloud   | --> |  Query   | --> |  Mapping  | --> |  Rules     | --> |  Report   |
|  API     |     |          |     |           |     |  Engine    |     |  Generator|
+----------+     +----------+     +-----------+     +------------+     +-----------+
     |                |                |                   |                  |
     | 1. Auth        | 2. JQL        | 3. Map to        | 4. Apply        | 5. Render  |
     |    Token       |    Query      |    Domain         |    Rules        |    HTML    |
     v                v                v                   v                  v
  Jira Cloud      /rest/api/3    Issue Entity        QualityRule        report.html
  API             /search?jql=   (Pydantic)          Engine
```

El sistema se ejecuta como una herramienta CLI que recibe un archivo de configuración, se conecta a Jira Cloud, recupera los issues especificados mediante JQL, los transforma a modelos de dominio, aplica reglas de calidad configurables, calcula el Backlog Quality Score (BQS) y genera un reporte HTML autocontenido con los resultados.

## Metas / No Metas

**Metas Funcionales:**
- Conexión a Jira Cloud via API REST con autenticación por token API
- Ejecución de consultas JQL con paginación automática
- Motor de reglas de calidad configurable via archivo YAML
- Evaluación individual de issues contra reglas predefinidas y personalizadas
- Cálculo del Backlog Quality Score (BQS) como métrica entre 0 y 100
- Desglose de puntuación por regla y por issue
- Generación de reporte HTML autocontenido con indicadores visuales
- Clasificación del backlog por umbrales de calidad configurables

**Metas No Funcionales:**
- Arquitectura Clean Architecture con 4 capas: Entities, Use Cases, Interface Adapters, Frameworks & Drivers
- Cobertura de pruebas unitarias > 80%
- Type hints en 100% del código
- Reporte HTML autocontenido sin dependencias externas de red
- Tiempo de ejecución < 5 minutos para backlogs de hasta 500 issues
- Configuración declarativa via YAML

**No Metas:**
- Análisis con IA (Claude) — será en versión futura
- Interfaz web interactiva o dashboard en tiempo real
- Modificación de issues en Jira (solo lectura)
- Soporte para Jira Server/Data Center
- Autenticación OAuth (solo token API)
- Despliegue como servicio (solo CLI)

## Decisiones

### Clean Architecture
Clean Architecture fue seleccionada porque el dominio del problema —evaluación de calidad de backlogs— tiene reglas de negocio estables (qué constituye un issue de calidad) que deben permanecer independientes de los detalles de infraestructura (API de Jira, formato de reporte, sistema de archivos). Esta separación permite:

- Probar la lógica de negocio sin depender de Jira ni del sistema de archivos.
- Reemplazar el proveedor de issues (Jira Cloud → Jira Server → API mock) sin modificar las entidades ni los casos de uso.
- Añadir análisis con IA (Claude) en el futuro como un caso de uso adicional sin alterar las capas existentes.
- Mantener las entidades de dominio puras (Pydantic) sin acoplamiento a frameworks externos.

### Capas de la arquitectura

```
+-------------------------------------------------------------------+
|                      Frameworks & Drivers                         |
|  (JiraApiClient, Jinja2Templates, FileSystem, YAMLLoader)         |
+-------------------------------------------------------------------+
|                     Interface Adapters                             |
|  (JiraIssueRepository, HtmlReportPresenter, CliController,         |
|   YAMLConfigLoader)                                                |
+-------------------------------------------------------------------+
|                         Use Cases                                  |
|  (FetchIssuesUseCase, EvaluateQualityUseCase,                      |
|   GenerateReportUseCase)                                           |
+-------------------------------------------------------------------+
|                          Entities                                  |
|  (Issue, Project, User, QualityRule, RuleResult, QualityReport)    |
+-------------------------------------------------------------------+
```

### Flujo de extremo a extremo

```
[CLI]                    [Use Cases]               [Adapters]              [Frameworks]
  |                          |                         |                        |
  |-- config.yaml ---------->|                         |                        |
  |                          |-- FetchIssuesUseCase -->|                        |
  |                          |                         |-- JiraApiClient ------>|
  |                          |                         |    (Jira Cloud API)    |
  |                          |                         |<-- Issues (JSON) ------|
  |                          |<-- Issue[] ------------|                        |
  |                          |                         |                        |
  |                          |-- EvaluateQualityUseCase                       |
  |                          |     |-- QualityRuleEngine                       |
  |                          |     |-- RuleResult[]                            |
  |                          |                         |                        |
  |                          |-- GenerateReportUseCase                        |
  |                          |                         |-- HtmlReportPresenter |
  |                          |                         |-- Jinja2 Template     |
  |                          |                         |-- report.html         |
  |<-- Reporte HTML ---------|                         |                        |
```

## Riesgos / Compensaciones

- **[Riesgo] Límites de tasa de Jira Cloud API** → Implementar throttling y paginación; configurar intervalo entre requests
- **[Riesgo] Issues con muchos campos** → Mapear solo los campos relevantes al modelo Issue; ignorar el resto
- **[Compensación] Inyección manual vs framework** → Más código boilerplate pero cero dependencias adicionales y máxima transparencia
- **[Riesgo] Reportes HTML muy grandes** → Paginación en el reporte o resumen ejecutivo con detalle colapsable
- **[Compensación] YAML para reglas** → Legible y versionable, pero sin validación estática fuerte (mitigado con Pydantic)

## Modelo de Dominio

El modelo de dominio representa los conceptos fundamentales del negocio. Son entidades puras sin dependencias de infraestructura, implementadas con Pydantic para validación automática y type hints.

### Issue

Representa un issue de Jira dentro del sistema. Contiene los campos relevantes para la evaluación de calidad:

```
Issue
├── id: str              -- ID interno de Jira
├── key: str             -- Clave del issue (ej: PROJ-123)
├── summary: str         -- Título del issue
├── description: str     -- Cuerpo del issue (puede estar vacío)
├── issue_type: str      -- Tipo (Story, Task, Bug, Epic, etc.)
├── priority: str        -- Prioridad (Highest, High, Medium, Low, Lowest)
├── status: str          -- Estado actual (To Do, In Progress, Done)
├── assignee: User       -- Usuario asignado (opcional)
├── reporter: User       -- Usuario reportador
├── labels: list[str]    -- Etiquetas del issue
├── created: datetime     -- Fecha de creación
├── updated: datetime     -- Fecha de última actualización
├── due_date: datetime   -- Fecha de vencimiento (opcional)
├── acceptance_criteria: str -- Criterios de aceptación (opcional)
├── estimation: float    -- Estimación en horas/puntos (opcional)
├── project: Project     -- Proyecto al que pertenece
├── components: list[str] -- Componentes
└── fix_versions: list[str] -- Versiones de corrección
```

### Project
Representa un proyecto de Jira. Contiene los metadatos necesarios para contextualizar los issues.

```
Project
├── id: str              -- ID interno de Jira
├── key: str             -- Clave del proyecto (ej: PROJ)
├── name: str            -- Nombre del proyecto
├── description: str     -- Descripción del proyecto (opcional)
├── lead: User           -- Líder del proyecto (opcional)
└── category: str        -- Categoría del proyecto (opcional)
```

### User
Representa un usuario de Jira. Se utiliza como referencia en Issue (assignee, reporter) y Project (lead).

```
User
├── account_id: str      -- ID de cuenta en Jira
├── display_name: str    -- Nombre visible
├── email: str           -- Correo electrónico (opcional)
└── active: bool         -- Indica si el usuario está activo
```

### QualityRule
Define una regla de calidad que se aplica a los issues. Es configurable y extensible.

```
QualityRule
├── name: str            -- Nombre único de la regla
├── description: str     -- Descripción de lo que evalúa
├── weight: int          -- Peso (0-100) para el cálculo del BQS
├── field: str           -- Campo del Issue a evaluar
├── condition: str       -- Condición a verificar (not_empty, present, valid_type, etc.)
├── error_message: str   -- Mensaje cuando la regla falla
└── enabled: bool        -- Permite deshabilitar la regla sin eliminarla
```

### RuleResult
Almacena el resultado de aplicar una regla a un issue específico.

```
RuleResult
├── rule_name: str       -- Nombre de la regla aplicada
├── issue_key: str       -- Clave del issue evaluado
├── passed: bool         -- Indica si la regla se cumplió
├── weight: int          -- Peso de la regla
├── message: str         -- Mensaje descriptivo (vacio si passed=True)
└── timestamp: datetime  -- Momento de la evaluación
```

### QualityReport
Contiene el resultado completo de la evaluación de un backlog. Es la entidad que se entrega al presentador para generar el reporte.

```
QualityReport
├── bqs: float                    -- Backlog Quality Score global (0-100)
├── total_issues: int             -- Número total de issues evaluados
├── total_rules: int              -- Número de reglas aplicadas
├── total_evaluations: int        -- Total de evaluaciones (issues × reglas)
├── passed_evaluations: int      -- Evaluaciones aprobadas
├── failed_evaluations: int       -- Evaluaciones falladas
├── score_by_rule: dict[str, float] -- BQS desglosado por regla
├── score_by_issue: dict[str, float] -- BQS desglosado por issue
├── results: list[RuleResult]    -- Resultados detallados
├── threshold: str               -- Clasificación (green/yellow/red)
├── jql_query: str               -- Consulta JQL utilizada
├── evaluated_at: datetime       -- Momento de la evaluación
└── config_snapshot: dict        -- Snapshot de la configuración usada
```

## Motor de Reglas

El motor de reglas es el componente central que evalúa la calidad de los issues. Está diseñado para ser extensible, configurable y fácil de mantener.

### Carga de reglas

Las reglas se definen en un archivo YAML con la siguiente estructura:

```yaml
rules:
  - name: description_not_empty
    description: "El issue debe tener una descripción no vacía"
    field: description
    condition: not_empty
    weight: 20
    enabled: true
    error_message: "El issue no tiene descripción"

  - name: acceptance_criteria_present
    description: "El issue debe tener criterios de aceptación"
    field: acceptance_criteria
    condition: present
    weight: 25
    enabled: true
    error_message: "El issue no tiene criterios de aceptación"
```

El sistema carga el archivo YAML al inicio, valida cada regla contra el esquema Pydantic y las registra en el motor de reglas. Si una regla tiene `enabled: false`, se omite durante la evaluación pero permanece disponible en la configuración.

### Validación de reglas

Cada regla se valida contra un modelo Pydantic `QualityRule` que verifica:
- `name`: debe ser único y no vacío
- `weight`: debe estar entre 1 y 100
- `field`: debe ser un campo válido del modelo Issue
- `condition`: debe ser una condición soportada por el motor
- `enabled`: booleano opcional (default: true)

Si alguna regla no pasa la validación, el sistema reporta el error con la regla específica y la razón del fallo, y detiene la ejecución.

### Ejecución de reglas

El motor de reglas itera sobre cada issue y aplica todas las reglas habilitadas:

```
por cada Issue en issues:
    por cada QualityRule en reglas habilitadas:
        resultado = evaluar(issue, regla)
        agregar resultado a RuleResult[]
```

Cada regla implementa una función de evaluación que recibe un Issue y retorna un booleano. Las condiciones soportadas inicialmente son:

| Condición | Descripción | Ejemplo de uso |
|---|---|---|
| `not_empty` | El campo no debe estar vacío | description, acceptance_criteria |
| `present` | El campo debe existir y no ser None | priority, assignee |
| `valid_type` | El issue_type debe estar en una lista permitida | story, task, bug, epic |
| `has_labels` | El issue debe tener al menos un label | labels |
| `has_estimation` | El issue debe tener estimación > 0 | estimation |

### Cálculo de puntuación

El motor calcula tres niveles de puntuación:

1. **Por evaluación**: cada regla aplicada a un issue produce un resultado (1 = pasa, 0 = falla).
2. **Por regla**: promedio de todas las evaluaciones de esa regla entre todos los issues.
3. **Por issue**: promedio ponderado de todas las reglas aplicadas a ese issue.
4. **Global (BQS)**: promedio ponderado de todas las evaluaciones.

```
BQS_global = (Σ_issues Σ_reglas (peso_r × resultado_i,r)) / (Σ_reglas peso_r × N_issues) × 100
```

### Extensibilidad

El motor de reglas está diseñado para ser extensible mediante un patrón de registro (registry pattern):

1. **Nuevas condiciones**: se añaden implementando una función `(Issue) -> bool` y registrándola en el motor.
2. **Reglas personalizadas**: los usuarios pueden definir reglas adicionales en el YAML usando condiciones existentes o nuevas.
3. **Reglas programáticas**: desarrolladores pueden implementar reglas en Python y registrarlas mediante un decorador o registro explícito.

## Requisitos No Funcionales

### Rendimiento
- El sistema debe completar la evaluación de un backlog de hasta 500 issues en menos de 5 minutos.
- La paginación de Jira debe ser paralelizable (múltiples requests simultáneos) para backlogs grandes.
- El reporte HTML debe generarse en menos de 5 segundos para 500 issues.
- El uso de memoria no debe exceder 500 MB para backlogs de hasta 1000 issues.

### Mantenibilidad
- Arquitectura Clean Architecture con dependencias estrictamente unidireccionales (Entities → Use Cases → Interface Adapters → Frameworks).
- Type hints en el 100% del código para facilitar el autocompletado y la detección temprana de errores.
- Cada clase debe tener una única responsabilidad (SRP).
- Nombres de clases, métodos y variables en inglés; documentación y mensajes de error en español.

### Escalabilidad
- El sistema está diseñado para backlogs de hasta 1000 issues por ejecución.
- La paginación de Jira permite manejar conjuntos de resultados grandes sin límite práctico.
- El motor de reglas es O(n × m) donde n = issues y m = reglas, lo que escala linealmente.
- Para backlogs mayores a 1000 issues, se puede ejecutar el análisis en lotes.

### Testabilidad
- Las entidades se prueban de forma aislada sin dependencias externas.
- Los casos de uso se prueban con repositorios y presentadores mock.
- Los adaptadores de infraestructura se prueban con integración real o con servidores mock (responses).
- Cobertura objetivo: > 80% según pytest-cov.
- Las pruebas no deben depender de una conexión real a Jira.

### Fiabilidad
- Reintentos automáticos ante errores transitorios de red (hasta 3 intentos con backoff exponencial).
- Validación de configuración al inicio para evitar fallos en tiempo de ejecución.
- Registro de errores con nivel de detalle configurable (DEBUG, INFO, WARNING, ERROR).
- El sistema nunca modifica datos en Jira (solo lectura).

### Seguridad
- Las credenciales de Jira se leen exclusivamente de variables de entorno, nunca del archivo YAML.
- Todas las comunicaciones con Jira Cloud usan HTTPS.
- El token API de Jira no se incluye en logs ni en el reporte HTML.
- El archivo de configuración YAML puede contener referencias a variables de entorno para credenciales.

## Manejo de Errores

El sistema implementa una jerarquía de excepciones personalizadas y una estrategia de manejo por capas, donde cada capa traduce las excepciones de la capa inferior a su propio nivel de abstracción.

### Jerarquía de excepciones

```
BacklogReviewError (base)
├── ConnectionError
│   ├── AuthenticationError    -- 401: credenciales inválidas
│   ├── AuthorizationError     -- 403: token sin permisos
│   ├── RateLimitError         -- 429: límite de tasa excedido
│   └── NetworkError           -- Timeout, DNS, conexión rechazada
├── JiraError
│   ├── InvalidJQLError        -- JQL malformado
│   └── IssueNotFoundError     -- Issue no encontrado
├── ConfigError
│   ├── YAMLParseError        -- YAML malformado
│   └── RuleValidationError   -- Regla inválida
└── ProcessingError
    └── PartialProcessingError -- Error en issue individual (no fatal)
```

### Estrategia de manejo por escenario

| Escenario | Detección | Acción |
|---|---|---|
| Autenticación fallida (401) | Respuesta HTTP 401 | Error inmediato sin reintento. Mensaje: "Error de autenticación. Verifica JIRA_EMAIL y JIRA_API_TOKEN." |
| Token sin permisos (403) | Respuesta HTTP 403 | Error inmediato sin reintento. Mensaje: "El token no tiene permisos para acceder al recurso solicitado." |
| Timeout de red | Excepción requests.Timeout | Reintento hasta 3 veces con backoff exponencial (1s, 2s, 4s). |
| Límite de tasa (429) | Respuesta HTTP 429 | Esperar header Retry-After y reintentar. |
| Error interno Jira (5xx) | Respuesta HTTP 5xx | Reintento hasta 2 veces. Si persiste, error con código. |
| JQL inválido | Respuesta HTTP 400 | Error inmediato con el mensaje de Jira y la consulta. |
| YAML malformado | Excepción yaml.YAMLError | Error con línea y columna del error de parseo. |
| Regla inválida | ValidationError (Pydantic) | Error con nombre de regla y campo inválido. |
| Issue individual falla | PartialProcessingError | Se omite el issue, se registra el error, se continúa con los demás. |

### Estrategia de reintentos

```
Error transitorio (timeout, 429, 5xx)
  └─► Reintento 1: esperar 1s
       └─► Reintento 2: esperar 2s
            └─► Reintento 3: esperar 4s
                 └─► Error permanente: abortar con mensaje
```

Errores permanentes (401, 403, 400) no se reintentan y abortan inmediatamente.

## Seguridad

### Gestión de tokens API

El token API de Jira se considera información sensible y se maneja con las siguientes políticas:

- **No en código**: el token nunca se hardcodea en el código fuente.
- **No en configuración**: el archivo YAML no contiene credenciales en texto plano.
- **Variables de entorno**: las credenciales se leen de `JIRA_EMAIL` y `JIRA_API_TOKEN`.
- **Referencias en YAML**: el archivo de configuración puede referenciar variables de entorno con sintaxis `${VAR_NAME}`.
- **Logs seguros**: el token se enmascara en logs de depuración (mostrar solo últimos 4 caracteres).

### Comunicaciones seguras

- Todas las comunicaciones con Jira Cloud API usan HTTPS con TLS 1.2 o superior.
- No se realizan llamadas a servicios externos no controlados.
- El reporte HTML generado no contiene credenciales ni información sensible.

### Variables de entorno

```
JIRA_SITE=https://tu-sitio.atlassian.net
JIRA_EMAIL=usuario@ejemplo.com
JIRA_API_TOKEN=tu-token-api
```

El archivo YAML de configuración referencia estas variables:

```yaml
jira:
  site: ${JIRA_SITE}
  email: ${JIRA_EMAIL}
  token: ${JIRA_API_TOKEN}
```

## Extensibilidad

La arquitectura está diseñada para evolucionar sin modificaciones disruptivas. Cada punto de extensión está protegido por una interfaz abstracta.

### Nuevas reglas de calidad

El motor soporta tres mecanismos de extensión:

1. **Configuración YAML**: los usuarios añaden reglas en el archivo de configuración usando condiciones existentes.
2. **Nuevas condiciones**: los desarrolladores registran nuevas funciones de evaluación en el `RuleRegistry`.
3. **Reglas programáticas**: los desarrolladores implementan subclases de `BaseRule` y las registran con un decorador.

```python
@rule_registry.register("has_due_date")
def has_due_date(issue: Issue) -> bool:
    return issue.due_date is not None
```

### Nuevos formatos de reporte

La interfaz `ReportPresenter` define el contrato para cualquier formato de salida:

```python
class ReportPresenter(ABC):
    @abstractmethod
    def present(self, report: QualityReport) -> str: ...
    @abstractmethod
    def output_extension(self) -> str: ...
```

Para añadir un nuevo formato (PDF, JSON, CSV, Markdown), se implementa esta interfaz y se registra en el caso de uso `GenerateReportUseCase`.

### Nuevos proveedores de Jira

La interfaz `IssueRepository` abstrae el origen de los issues:

```python
class IssueRepository(ABC):
    @abstractmethod
    def fetch_by_jql(self, jql: str) -> list[Issue]: ...
    @abstractmethod
    def get_by_key(self, key: str) -> Issue: ...
```

Para soportar Jira Server, Azure DevOps u otro proveedor, se implementa un nuevo repositorio que implemente esta interfaz.

### Integración futura con Claude

La arquitectura permite añadir análisis con IA en tres pasos sin modificar el código existente:

1. **Nuevo adaptador**: `ClaudeApiClient` en Frameworks & Drivers para comunicarse con Claude API.
2. **Nuevo caso de uso**: `AIQualityAnalysisUseCase` que recibe los issues y los resultados del motor de reglas, y enriquece el análisis con recomendaciones semánticas.
3. **Nuevo presentador**: `AIHtmlReportPresenter` que extiende el reporte HTML con secciones de análisis IA.

```
Estado actual:
  Reglas sintácticas → BQS → Reporte HTML

Con IA (futuro):
  Reglas sintácticas → BQS base
  + Análisis semántico (Claude) → BQS enriquecido
  → Reporte HTML con recomendaciones IA
```