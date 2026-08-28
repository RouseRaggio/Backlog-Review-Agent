## 1. AI Provider Interface (Domain Layer)

- [ ] 1.1 Create `src/domain/ai/__init__.py` package
- [ ] 1.2 Define `AIProvider` abstract base class with `generate()`, `default_model`, and concrete `health()` method in `src/domain/ai/ai_provider.py`
- [ ] 1.3 Define `HealthStatus` dataclass in `src/domain/ai/health_status.py`
- [ ] 1.4 Add unit tests for interface contract (can't instantiate ABC, method signatures, default health returns unreachable)

## 2. Domain Entities

- [ ] 2.1 Create `AiExecutiveSummary` and `PriorityAction` dataclasses in `src/domain/entities/ai_executive_summary.py`
- [ ] 2.2 Add optional `ai_summary: AiExecutiveSummary | None` field to `AuditReport` entity
- [ ] 2.3 Update all existing `AuditReport` instantiations to pass the new field (default `None`)
- [ ] 2.4 Add unit tests for AiExecutiveSummary construction and AuditReport backward compatibility

## 3. Configuration System (Infrastructure Layer)

- [ ] 3.1 Define `AppConfig`, `AiConfig`, `CapabilityConfig`, `OpenAiProviderConfig`, `AnthropicProviderConfig`, `OllamaProviderConfig` dataclasses in `src/infrastructure/configuration/`
- [ ] 3.2 Implement `ConfigLoader` class in `src/infrastructure/configuration/config_loader.py` with YAML parsing
- [ ] 3.3 Update `config/config.example.yaml` with the `ai:` section (enabled, provider, model, timeout, max_tokens, temperature, rate_limit_rpm, rate_limit_queue, prompt_dir, capabilities, provider-specific configs)
- [ ] 3.4 Add unit tests for ConfigLoader (valid YAML, missing file, malformed YAML, env var override)

## 4. Prompt Template System (Domain + Infrastructure)

- [ ] 4.1 Create `PromptRenderer` domain interface in `src/domain/ai/prompt_renderer.py` with `render(template_text, params) -> str` using `str.replace()` for `{{placeholder}}` substitution
- [ ] 4.2 Create `PromptLoader` infrastructure service in `src/infrastructure/ai/prompt_loader.py` that reads prompt files from a configurable directory
- [ ] 4.3 Create prompt template files in `prompts/` directory:
  - `prompts/executive_summary.txt`
  - `prompts/story_quality.txt` (placeholder for future capability)
  - `prompts/ac_generation.txt` (placeholder for future capability)
- [ ] 4.4 Add unit tests for PromptRenderer (substitution, missing params, extra params ignored)
- [ ] 4.5 Add unit tests for PromptLoader (file found, file not found, custom directory)

## 5. Provider Implementations (Infrastructure Layer)

- [ ] 5.1 Create `src/infrastructure/ai/__init__.py` package
- [ ] 5.2 Implement `OpenAIProvider` in `src/infrastructure/ai/openai_provider.py` with `health()` override (List Models endpoint)
- [ ] 5.3 Implement `AnthropicProvider` in `src/infrastructure/ai/anthropic_provider.py` with `health()` override (Messages API ping)
- [ ] 5.4 Implement `OllamaProvider` in `src/infrastructure/ai/ollama_provider.py` with `health()` override (`/api/tags` GET)
- [ ] 5.5 Implement `AIProviderFactory` in `src/infrastructure/ai/provider_factory.py`
- [ ] 5.6 Add `openai`, `anthropic`, `httpx` to `requirements.txt`
- [ ] 5.7 Add unit tests with mocked HTTP/SDK for each provider `generate()` and `health()`, and factory

## 6. Infrastructure Retry and Rate Limiting

- [ ] 6.1 Implement retry wrapper in `src/infrastructure/ai/retry_wrapper.py` (3 retries, exponential backoff 1s/2s/4s, ±250ms jitter, no retry on 4xx)
- [ ] 6.2 Define `RateLimitExceeded` exception in `src/infrastructure/ai/rate_limiter.py`
- [ ] 6.3 Implement rate limiter wrapper in `src/infrastructure/ai/rate_limiter.py` (configurable RPM, request queue, queue full → RateLimitExceeded)
- [ ] 6.4 Add unit tests for retry wrapper (transient retried, 4xx not retried, all retries exhausted)
- [ ] 6.5 Add unit tests for rate limiter (under limit passes, over limit queued, queue full rejected)

## 7. AIReviewEngine (Application Layer)

- [ ] 7.1 Define `AICapabilityOutput` base dataclass and `SchemaValidationError` exception in `src/application/ai/`
- [ ] 7.2 Define `AICapability` dataclass in `src/application/ai/capability.py` (id, name, prompt_template, output_schema)
- [ ] 7.3 Implement `AIReviewEngine` class in `src/application/ai/ai_review_engine.py` with `execute(capability_id, input_data) -> AICapabilityOutput | None`
- [ ] 7.4 Implement the execution flow: capability lookup → config resolution → prompt load → prompt render → provider call (with capability-specific model/temperature/max_tokens) → JSON parse → schema validation → return output or None
- [ ] 7.5 Implement error handling: log all errors with correlation ID, return None for all failure modes
- [ ] 7.6 Add unit tests for AIReviewEngine (successful execution, unknown capability, provider failure, validation failure)

## 8. GenerateExecutiveSummary Use Case (Application Layer)

- [ ] 8.1 Create `src/application/use_cases/ai_executive_summary.py`
- [ ] 8.2 Implement `GenerateExecutiveSummary.execute(report) -> AiExecutiveSummary` with prompt building, AI call, and JSON parsing
- [ ] 8.3 Implement fail-open behavior (log error, return None on exception)
- [ ] 8.4 Add unit tests with mock AIProvider (success, unparseable response, exception)

## 9. Dependency Injection (Bootstrap)

- [ ] 9.1 Update `build_application()` in `src/bootstrap/dependency_injection.py` with the following sequence:
  1. Load `AppConfig` via `ConfigLoader.load()`
  2. If `config.ai.enabled` is False, skip AI init, pass `AIReviewEngine=None` to use case
  3. Create provider config from config section matching `config.ai.provider`
  4. Create provider via `AIProviderFactory.create()`
  5. Call `provider.health()` — if fails, log warning and disable AI
  6. Wrap provider with `RetryWrapper`
  7. Wrap provider with `RateLimiter`
  8. Create `PromptLoader` with `config.ai.prompt_dir`
  9. Create `PromptRenderer`
  10. Register capabilities dict (`{"executive_summary": AICapability(...)}`)
  11. Generate correlation ID via `uuid.uuid4().hex[:12]`
  12. Create `AIReviewEngine` with all dependencies
  13. Pass `AIReviewEngine` to `AuditBacklogUseCase`
- [ ] 9.2 Add bootstrap tests (AI enabled full wiring, health check failure degrades, AI disabled skips init)

## 10. HTML Dashboard Integration

- [ ] 10.1 Design and add "AI Executive Summary" card HTML block above the charts grid in `report.html`
- [ ] 10.2 Create AI icon SVG (turquoise, distinct from existing icons)
- [ ] 10.3 Add conditional rendering logic (`{{AI_SUMMARY_JSON}}` placeholder, hide when empty)
- [ ] 10.4 Update `HtmlReportGenerator.generate()` to serialize `AiExecutiveSummary` to JSON and inject into template
- [ ] 10.5 Update `HtmlReportGenerator._build_findings()` (no structural changes, just verify compatibility)
- [ ] 10.6 Verify generated HTML renders AI section correctly and hides when absent

## 11. CLI Integration

- [ ] 11.1 Update `print_summary()` in `src/presentation/cli/__init__.py` to display AI summary when available
- [ ] 11.2 Verify CLI output with and without AI summary

## 12. Integration Tests

- [ ] 12.1 Write end-to-end test: deterministic audit + AI summary with mocked provider
- [ ] 12.2 Write end-to-end test: AI disabled produces same report as before
- [ ] 12.3 Write end-to-end test: AI provider failure degrades gracefully (health fail, retry exhaust, validation fail)
- [ ] 12.4 Write end-to-end test: full bootstrap wiring produces configured AIReviewEngine
