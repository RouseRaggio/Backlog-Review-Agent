## Why

The current rule engine evaluates backlog quality purely through deterministic field checks (has description, has priority, is assigned, etc.). While effective for structural validation, it cannot assess semantic quality, coherence, or provide intelligent recommendations. An AI Review Engine enriches the analysis by adding LLM-powered insights that complement — not replace — the existing deterministic rules, giving teams actionable, context-aware guidance.

## What Changes

- Introduce an `AIProvider` abstraction (interface) so different LLM backends can be swapped without changing application code.
- Implement a new `GenerateExecutiveSummary` use case that takes a `QualityReport` and returns a concise AI-generated executive summary.
- Add an AI Executive Summary section to the HTML dashboard, displayed above the charts and visually distinguished with an AI icon.
- Extend configuration to support enabling/disabling AI, selecting the provider, and setting the model name.
- Create a pluggable provider architecture that supports OpenAI, Anthropic, and Ollama initially.
- Lay the architectural groundwork for future AI capabilities (story quality review, AC generation, backlog prioritization, etc.) without committing to their implementation.

## Capabilities

### New Capabilities
- `ai-provider-interface`: Abstract contract for LLM providers with methods for text generation, supporting OpenAI, Anthropic, and Ollama adapters.
- `ai-executive-summary`: Use case that analyzes `AuditReport` findings and produces a structured executive summary (overall quality, most critical findings, priority actions).
- `ai-configuration`: Configuration model and YAML loading for AI provider selection, model name, enable/disable toggle, and provider-specific settings.

### Modified Capabilities
- *(None — no existing specs are being changed.)*

## Impact

- **New dependency**: `openai`, `anthropic` Python SDKs; `httpx` or `requests` for Ollama.
- **Domain**: New domain entity (`AiExecutiveSummary`) and/or service interface (`AiProvider`).
- **Application**: New use case (`GenerateExecutiveSummary`). `AuditBacklogUseCase` may orchestrate AI analysis after deterministic evaluation.
- **Infrastructure**: New provider adapters (`OpenAiProvider`, `AnthropicProvider`, `OllamaProvider`). Config loader extended for AI settings.
- **Presentation**: HTML report template updated with AI Executive Summary card. CLI extended to show AI summary.
- **Bootstrap**: DI container wired with AI provider and optional AI toggle.
- **No breaking changes**: Existing rules, scoring, and report generation remain untouched.
