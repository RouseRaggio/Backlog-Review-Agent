## Context

The Backlog Review Agent evaluates Jira backlog quality using 10 deterministic rules (field-presence checks). The `AuditBacklogUseCase` orchestrates issue retrieval, rule evaluation, and scoring. The result is an `AuditReport` containing structured findings and a Backlog Quality Score (0-100). A static HTML dashboard visualizes the report.

There is no AI integration today. The `Rule` entity has an unused `requires_ai` field, and the config YAML is defined but not loaded at runtime. The project uses Clean Architecture with manual dependency injection.

This design adds an AI Review Engine that complements the deterministic engine. It introduces an `AIProvider` abstraction, a new use case for generating executive summaries, HTML dashboard integration, and a YAML-based configuration system extended for AI settings.

## Goals / Non-Goals

**Goals:**
- Define an `AIProvider` interface that supports OpenAI, Anthropic, and Ollama.
- Implement `GenerateExecutiveSummary` use case that consumes `AuditReport` and returns a structured summary.
- Display the AI Executive Summary in the HTML dashboard above the charts with an AI icon.
- Load AI configuration from a YAML file (enable/disable, provider selection, model name, provider-specific options).
- Wire everything through Clean Architecture: domain knows nothing about AI SDKs; infrastructure contains all provider implementations.
- Lay extensibility foundation for future AI capabilities (story quality, AC generation, prioritization, sprint recommendations).

**Non-Goals:**
- Replace or modify any existing deterministic rules.
- Implement future AI capabilities beyond the executive summary.
- Change the scoring algorithm.
- Modify the existing `AuditReport` entity schema.
- Add streaming responses or interactive chat.

## Decisions

### D1 — AIProvider as a Protocol (ABC) in Domain

Define `ai_provider.py` in the domain layer as a Python `Protocol` or `ABC`:

```python
class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, model: str | None = None, **kwargs) -> str: ...
    @property
    @abstractmethod
    def default_model(self) -> str: ...
```

**Rationale:** The domain layer defines the contract so that application use cases depend only on the abstraction. Infrastructure implements the contract for each LLM backend. This follows Clean Architecture: domain is SDK-agnostic.

**Alternatives considered:**
- Define `AIProvider` in the application layer: Rejected because it would force application to own an interface that multiple implementations (infrastructure) must satisfy. Domain is the correct owner for provider contracts.
- No interface, direct SDK calls in use case: Rejected because it violates Clean Architecture and makes testing impossible without network calls.

### D2 — Provider Implementations in Infrastructure

Each provider gets its own file under `src/infrastructure/ai/`:

```
infrastructure/
  ai/
    __init__.py
    openai_provider.py       # OpenAI SDK adapter
    anthropic_provider.py    # Anthropic SDK adapter
    ollama_provider.py       # Ollama HTTP adapter
```

**Rationale:** Infrastructure layer owns all external integrations. Separating providers by file keeps each adapter focused and testable in isolation.

**Provider-specific notes:**
- **OpenAI**: Uses `openai` SDK. Chat Completions endpoint with `gpt-4o-mini` as default.
- **Anthropic**: Uses `anthropic` SDK. Messages API with `claude-3-haiku` as default.
- **Ollama**: Uses `httpx` for HTTP calls to `http://localhost:11434/api/generate`. No SDK dependency.

### D3 — GenerateExecutiveSummary Use Case in Application Layer

New use case `GenerateExecutiveSummary` in `src/application/use_cases/ai_executive_summary.py`:

```
Input:  AuditReport
Output: AiExecutiveSummary (domain entity)
Flow:
  1. Build a structured prompt from the AuditReport data
  2. Call AIProvider.generate(prompt)
  3. Parse the LLM response into AiExecutiveSummary
  4. Return the summary
```

**Rationale:** Application layer orchestrates the AI call without knowing provider details. The use case is testable by injecting a mock `AIProvider`.

**Prompt design:** The prompt includes:
- Project name and total issue count
- Quality score and breakdown (PASS/FAIL/WARNING/BLOCKED)
- Top 5 failed rules by count with severities
- List of findings grouped by severity
- Instructions to produce a 3-paragraph summary: overall quality assessment, most critical findings, top 3 priority actions
- The response is expected as structured JSON (`{ "overall_assessment": "...", "critical_findings": ["..."], "priority_actions": [{"action": "...", "rationale": "..."}] }`)

### D4 — AiExecutiveSummary Domain Entity

New entity in `src/domain/entities/ai_executive_summary.py`:

```python
@dataclass
class AiExecutiveSummary:
    overall_assessment: str
    critical_findings: list[str]
    priority_actions: list[PriorityAction]

@dataclass
class PriorityAction:
    action: str
    rationale: str
```

**Rationale:** A typed domain entity ensures the application and presentation layers work with structured data, not raw strings. It preserves Clean Architecture boundaries.

### D5 — YAML Configuration for AI Settings

Extend `config/config.yaml` (loaded at runtime) with an `ai` section:

```yaml
ai:
  enabled: true
  provider: openai          # openai | anthropic | ollama
  model: gpt-4o-mini        # provider-specific default
  openai:
    api_key_env: OPENAI_API_KEY
    organization: ~
  anthropic:
    api_key_env: ANTHROPIC_API_KEY
  ollama:
    base_url: http://localhost:11434
    model: llama3
```

Implement a `ConfigLoader` in infrastructure that reads this YAML and returns typed config objects. The existing `JiraConfig` pattern (env-only) is superseded by a unified config.

**Rationale:** YAML is explicit, version-controllable, and supports nested provider-specific settings. Environment variables for secrets (API keys) are referenced by name rather than embedded.

**Alternatives considered:**
- Extend `.env` with AI keys: Rejected because provider selection, model names, and multi-provider settings are more naturally expressed in structured YAML.

### D6 — Orchestration in AuditBacklogUseCase

After deterministic evaluation, if AI is enabled, the use case optionally calls `GenerateExecutiveSummary`:

```
execute() -> AuditReport:
  1. issues = jira_client.get_issues(...)
  2. findings = rule_engine.evaluate(issues)
  3. report = AuditReport(...)
  4. if ai_config.enabled:
       ai_summary = ai_summary_use_case.execute(report)
       report.ai_summary = ai_summary
  5. return report
```

**Rationale:** Keeping AI orchestration in the existing use case avoids a separate execution path. The `AuditReport` entity gains an optional `ai_summary` field.

### D7 — Dashboard Integration

A new "AI Executive Summary" card is added to the HTML template above the charts section. It displays:
- A turquoise AI icon (distinct from the existing warning/error icons)
- The overall assessment text
- Critical findings as a bullet list
- Priority actions with rationale

The section is conditionally rendered: if `{{AI_SUMMARY_JSON}}` is empty, the section is hidden. The generator serializes `AiExecutiveSummary` to JSON and injects it into the template.

**Rationale:** The AI summary appears prominently above the charts because it's the highest-value insight. Conditional rendering ensures backward compatibility when AI is disabled.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| **LLM latency** slows report generation (3-10 seconds per summary) | AI runs after deterministic evaluation; timeout configurable; AI can be disabled entirely via config |
| **LLM cost** with large backlogs | Prompt is optimized to include only summary statistics, not raw issues; model selection (haiku/gpt-4o-mini) minimizes cost; AI can be disabled |
| **Non-deterministic output** — AI may produce different summaries for the same data | Prompt instructs strict JSON format; parser validates structure; fallback to template text if parsing fails |
| **API key management** — providers require different auth | Keys loaded from environment variables, never logged; provider config references env var names |
| **Ollama not running** when selected | Provider instantiation validates connectivity; use case raises clear `ConnectionError`; graceful degradation falls back to no-AI mode |
| **Prompt injection** through backlog data | Prompt templates sanitize issue data to text only; structured output parsing limits injection surface |
