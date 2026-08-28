# Design: Test Case Generator Agent Architecture

## Architectural Context

```text
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│                                                        │
│  ┌───────────────────────┐   ┌──────────────────────┐  │
│  │   React Dashboard     │   │     FastAPI App      │  │
│  │  (Port 5174/Nginx)    │   │     (Port 8001)      │  │
│  └───────────┬───────────┘   └──────────┬───────────┘  │
└──────────────┼──────────────────────────┼──────────────┘
               │                          │
               ▼                          ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│                                                        │
│               GenerateTestCasesUseCase                 │
│         (Orchestration, Sufficiency & Metrics)         │
└──────────────────────┬─────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌──────────────────┐       ┌──────────────────┐
│   Domain Layer   │       │  Infrastructure  │
│                  │       │                  │
│   UserStory      │       │ RuleBasedTestCase│
│   AcceptanceCrit │◄──────┤ Generator        │
│   TestCase       │ (Port)│                  │
│   GenerationRes  │       │ LLMTestCase      │
│   SufficiencyVal │       │ Generator (Stub) │
│   TraceabilitySvc│       │                  │
└──────────────────┘       └──────────────────┘
```

## Evidence & Generation Model

### 1. Evidence Verification
- **Positive Scenarios**: Derived directly from explicit action capabilities (e.g. "El administrador puede crear un usuario con nombre, correo y rol").
- **Negative Scenarios**: Generated **only** when explicitly justified:
  - Uniqueness constraints (e.g. "El correo electrónico debe ser único" $\to$ duplicate email test case).
  - Explicitly required fields (e.g. "proporcionando obligatoriamente..." $\to$ missing mandatory field test case).
  - Explicit business rejection rules (e.g. "No se permite desactivar usuarios con tareas activas").
- **Validation Scenarios**: Generated for explicit system validation messages or notifications.
- **Boundary Scenarios**: Generated **strictly** when numbers, ranges, minimum/maximum lengths, or date boundaries are present (e.g. "entre 3 y 50 caracteres" $\to$ 3, 50, 2, 51). If no numbers/limits exist, boundary generation is omitted and an explicit warning is appended.

### 2. Confidence Model
- **`HIGH`**: Scenario is directly backed by an explicit Acceptance Criterion.
- **`MEDIUM`**: Scenario is derived from the User Story text without dedicated Acceptance Criteria.
- **`LOW`**: Information is insufficient or incomplete.

### 3. Traceability Mapping
Each `TestCase` contains:
- `requirement_reference`: Project/Issue Key (e.g. `GES-123`).
- `acceptance_criteria_reference`: Criterion ID (e.g. `AC-001`) or `"USER_STORY"`.
`TraceabilityService` calculates the percentage of criteria covered and constructs a bidirectional coverage map.
