# Design: Web Interface for Backlog Review Agent

## Architectural Context
The Backlog Review Agent follows Clean Architecture. The web interface introduces a new presentation adapter (`src/presentation/api/`) alongside the existing CLI and HTML generator presentation adapters, without modifying the inner application and domain layers.

```text
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│                                                        │
│  ┌───────────────────────┐   ┌──────────────────────┐  │
│  │   CLI / HTML Report   │   │     FastAPI App      │  │
│  │  (main.py, generator) │   │ (src/presentation/api)│  │
│  └───────────┬───────────┘   └──────────┬───────────┘  │
└──────────────┼──────────────────────────┼──────────────┘
               │                          │
               ▼                          ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│                                                        │
│                  AuditBacklogUseCase                   │
└──────────────────────┬─────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌──────────────────┐       ┌──────────────────┐
│   Domain Layer   │       │  Infrastructure  │
│                  │       │                  │
│   RuleEngine     │       │    JiraClient    │
│   ScoreService   │       │    JiraConfig    │
│   AuditReport    │       │                  │
│   Finding        │       │                  │
└──────────────────┘       └──────────────────┘
```

## Component Breakdown

### 1. Presentation API (`src/presentation/api/`)
- **`schemas.py`**: Presentation Data Transfer Objects (DTOs) built using Pydantic v2.
  - `ReviewRequest`: Validates `project_key` (non-empty string, stripped) and `max_results` (integer between 1 and 1000, default 100).
  - `ProjectDTO`: `key: str`, `name: Optional[str] = None`.
  - `StatisticsDTO`: `total_issues: int`, `total_findings: int`, `passed: int`, `warnings: int`, `failed: int`, `blocked: int`.
  - `FindingDTO`: `rule_id: str`, `rule_name: str`, `issue_key: str`, `issue_type: str`, `status: str`, `severity: Optional[str] = None`, `message: str`, `recommendation: Optional[str] = None`.
  - `ReviewResponse`: `project: ProjectDTO`, `quality_score: float`, `statistics: StatisticsDTO`, `findings: list[FindingDTO]`.
  - `ErrorResponse`: `detail: str`, `error_type: str`.
- **`mappers.py`**: Pure mapping functions converting `AuditReport` domain entities into `ReviewResponse` DTOs. Computes `total_issues = len({f.issue_key for f in report.findings})`.
- **`routes.py`**: Endpoint definitions (`POST /api/reviews`). Injects `AuditBacklogUseCase` using dependency injection (`build_application`).
- **`app.py`**: FastAPI application setup with configured CORS origins (`http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:3000`).

### 2. Frontend Application (`apps/backlog-review-agent/frontend/`)
- **`src/types/api.ts`**: TypeScript definitions reflecting the API schemas.
- **`src/services/api.ts`**: HTTP client interacting with the backend API.
- **`src/components/ReviewForm.tsx`**: Controlled form inputs for project key and max results, validation, and submission trigger with loading state.
- **`src/components/ScoreGauge.tsx`**: Score visualization component with color indicator according to BQS.
- **`src/components/StatsCards.tsx`**: Metric summary cards (Total Issues, Total Findings, Passed, Warnings, Failed, Blocked).
- **`src/components/FindingsTable.tsx`**: Searchable and filterable table displaying findings with badges.
- **`src/components/FindingDetailModal.tsx`**: Modal displaying complete finding information when a row is selected.
- **`src/App.tsx`**: Top-level state and layout coordination.

## Error Handling Strategy
- **Client Validation Errors (422)**: Pydantic automatically handles malformed payloads and returns structured validation messages.
- **Jira Connectivity / Upstream Errors (502 / 500)**: Captured in routes and mapped to clean `ErrorResponse` JSON without leaking Jira auth tokens, emails, or internal stack traces.
