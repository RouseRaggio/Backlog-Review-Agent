# Design: Jira Integration & Analysis Architecture

## Architectural Context

```text
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│                                                        │
│  - POST /api/test-cases/analyze                        │
│  - POST /api/test-cases/generate (Jira / Manual)       │
│  - React Dashboard (Jira Input, Preview, Fallback)     │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
               ▼                          ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│                                                        │
│  - AnalyzeUserStoryUseCase (Jira fetch & parsing)      │
│  - GenerateTestCasesUseCase (Orchestration & fallback) │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
         ┌─────┴─────────────┐            ▼
         ▼                   ▼   ┌──────────────────────┐
┌──────────────────┐ ┌───────────┤    Infrastructure    │
│   Domain Layer   │ │ (Port)    │                      │
│                  │ │JiraGateway│- JiraClient (REST)   │
│ - UserStory      │ └───────────┤- CriteriaExtractor   │
│ - AcceptanceCrit │             │- JiraConfig          │
│ - TestCase       │             │- RuleBasedGenerator  │
│ - GenerationRes  │             └──────────────────────┘
└──────────────────┘
```

## Jira Extraction & Mapping Strategy

### 1. Issue Retrieval
- Calls Jira REST API `GET /rest/api/3/issue/{issue_key}`.
- Sanitizes and extracts text from Atlassian Document Format (ADF) or plain string.
- Error handling maps HTTP status codes:
  - `404` $\to$ `UserStoryNotFoundError` ("Historia de Usuario no encontrada en Jira.")
  - `401`/`403` $\to$ `JiraPermissionError` ("No tienes permisos para consultar esta Issue.")
  - `500`/`502`/`503` $\to$ `JiraConnectionError` ("No fue posible comunicarse con Jira.")
  - `Timeout` $\to$ `JiraTimeoutError` ("Jira no respondió dentro del tiempo esperado.")
  - Missing URL/Credentials $\to$ `JiraConfigError` ("La integración con Jira no está configurada correctamente.")

### 2. Criteria Extraction (`CriteriaExtractor`)
- **Primary Source (Custom Field)**: If `JIRA_ACCEPTANCE_CRITERIA_FIELD` is configured and present in `fields`.
- **Secondary Source (Description Parsing)**:
  - Scans for headers: `Criterios de Aceptación:`, `Acceptance Criteria:`, `Criterios:`, `Condiciones:`.
  - Parses numbered lists (`1.`, `2.`), bullet lists (`-`, `*`), Gherkin blocks (`Dado/Cuando/Entonces`, `Given/When/Then`), or explicit labels (`AC-001`, `AC-1`).
  - Normalizes IDs to `AC-001`, `AC-002`, etc.
  - If no criteria are found, returns an empty list, allowing `SufficiencyValidator` to issue warnings and degrade confidence.

### 3. Use Case Decision (`AnalyzeUserStoryUseCase` vs `GenerateTestCasesUseCase`)
- `AnalyzeUserStoryUseCase`: Dedicated query use case for previewing parsed story and criteria before generation.
- `GenerateTestCasesUseCase`: Orchestrates end-to-end generation. If manual story/criteria are passed, it uses them; otherwise it fetches them from Jira via `JiraGateway`.
