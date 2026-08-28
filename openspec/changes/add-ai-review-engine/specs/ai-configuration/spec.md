## ADDED Requirements

### Requirement: Unified YAML configuration loader

The system SHALL implement a `ConfigLoader` in the infrastructure layer that reads a YAML configuration file and returns typed configuration objects.

The loader SHALL:
- Read from `config/config.yaml` by default
- Support an override path via environment variable `BQS_CONFIG_PATH`
- Return a `AppConfig` dataclass with nested `JiraConfig` and `AiConfig` sections
- Raise `FileNotFoundError` if the config file does not exist
- Raise `yaml.YAMLError` if the file is malformed

#### Scenario: Config file loaded successfully

- **WHEN** a valid `config/config.yaml` exists
- **AND** `ConfigLoader.load()` is called
- **THEN** it SHALL return an `AppConfig` instance with all fields populated from the YAML

#### Scenario: Missing config file raises error

- **WHEN** `ConfigLoader.load(path="/nonexistent.yaml")` is called
- **THEN** it SHALL raise `FileNotFoundError`

#### Scenario: Custom config path via environment variable

- **WHEN** the environment variable `BQS_CONFIG_PATH` is set to `/custom/path/config.yaml`
- **AND** `ConfigLoader.load()` is called with no path argument
- **THEN** it SHALL read from `/custom/path/config.yaml`

### Requirement: AiConfig dataclass

The system SHALL define an `AiConfig` dataclass that represents the `ai:` section of the configuration YAML.

The dataclass SHALL have the following fields with defaults:

```python
@dataclass
class CapabilityConfig:
    temperature: float = 0.3
    max_tokens: int = 1024
    model: str | None = None          # overrides provider-level model

@dataclass
class AiConfig:
    enabled: bool = False
    provider: str = "openai"          # openai | anthropic | ollama
    model: str | None = None          # provider-specific default
    timeout: int = 30
    max_tokens: int = 1024
    temperature: float = 0.3
    rate_limit_rpm: int = 30
    rate_limit_queue: int = 10
    prompt_dir: str = "prompts"
    capabilities: dict[str, CapabilityConfig] = field(default_factory=dict)
    openai: OpenAiProviderConfig | None = None
    anthropic: AnthropicProviderConfig | None = None
    ollama: OllamaProviderConfig | None = None
```

Provider-specific configs SHALL contain the fields needed for that provider (API key env var names, base URLs, etc.).

#### Scenario: AiConfig parsed from YAML

- **WHEN** a YAML file contains an `ai:` section with `enabled: true`, `provider: anthropic`
- **THEN** `AiConfig.enabled` SHALL be `True`
- **AND** `AiConfig.provider` SHALL be `"anthropic"`

#### Scenario: AiConfig defaults when section missing

- **WHEN** the YAML file has no `ai:` section
- **THEN** `AiConfig` SHALL use all default values
- **AND** `enabled` SHALL be `False`

### Requirement: AI configuration toggle

The system SHALL allow enabling or disabling AI analysis through the `ai.enabled` configuration flag.

When `ai.enabled` is `False`:
- The `AuditBacklogUseCase` SHALL NOT invoke any AI use case
- The HTML dashboard SHALL NOT display any AI section
- The CLI SHALL NOT print any AI output

When `ai.enabled` is `True`:
- The application SHALL use the configured provider and model to generate the AI executive summary
- If the provider cannot be initialized (missing API key, connection failure), the application SHALL log a warning and continue without AI

#### Scenario: AI disabled — no AI overhead

- **WHEN** `config.ai.enabled` is `False`
- **THEN** no AI provider SHALL be initialized
- **AND** report generation SHALL proceed exactly as before

#### Scenario: AI enabled but provider fails

- **WHEN** `config.ai.enabled` is `True`
- **AND** the configured provider throws on initialization
- **THEN** the application SHALL log the initialization failure
- **AND** continue without AI (fail-open)

### Requirement: Provider selection via configuration

The system SHALL allow selecting the AI provider through the `ai.provider` configuration field.

Valid values SHALL be `"openai"`, `"anthropic"`, and `"ollama"`.

An invalid value SHALL cause a `ValueError` at application startup.

#### Scenario: Provider selected from config

- **WHEN** `config.ai.provider` is `"ollama"`
- **THEN** the factory SHALL create an `OllamaProvider` instance

#### Scenario: Invalid provider raises error

- **WHEN** `config.ai.provider` is `"invalid"`
- **THEN** the bootstrap layer SHALL raise a `ValueError`

### Requirement: Model name configuration

The system SHALL allow overriding the default model per provider through `config.ai.model`.

If `config.ai.model` is `None`, each provider SHALL use its hardcoded default model.

#### Scenario: Custom model name used

- **WHEN** `config.ai.model` is `"gpt-4"`
- **AND** the provider is `"openai"`
- **THEN** `OpenAIProvider.generate()` SHALL use `model="gpt-4"`

#### Scenario: Default model when model is null

- **WHEN** `config.ai.model` is `None`
- **AND** the provider is `"openai"`
- **THEN** `OpenAIProvider` SHALL use `"gpt-4o-mini"` as the model

### Requirement: Prompt template management

The system SHALL manage AI prompts as versioned, parameterized templates rather than hardcoded strings.

Prompts SHALL be defined in a dedicated `prompts/` directory at the project root, one file per use case, using `{{placeholder}}` syntax with Python's built-in `str.replace()` for substitution. No third-party template library (Jinja2, Mako, etc.) SHALL be added as a dependency.

Each prompt template SHALL:
- Have a unique filename matching the use case name (e.g., `executive_summary.txt`)
- Be loaded at runtime by a `PromptRenderer` service
- Accept typed parameters that the use case fills before sending to the AI provider
- Include instructions for the LLM response format (JSON schema expected)

The `PromptRenderer` SHALL reside in the domain layer and SHALL NOT depend on any AI provider or file-system logic. File loading SHALL be an infrastructure concern.

The domain `PromptRenderer` SHALL accept `(template_text: str, params: dict[str, str]) -> str`. The infrastructure file loader SHALL read the file and pass its content to the renderer.

#### Scenario: Prompt template loaded and rendered

- **WHEN** `PromptRenderer.render("executive_summary", {"score": 72, "fail_count": 5})` is called
- **THEN** it SHALL return a string with `{{score}}` replaced by `72` and `{{fail_count}}` replaced by `5`

#### Scenario: Missing template raises error

- **WHEN** `PromptRenderer.render("nonexistent")` is called
- **THEN** it SHALL raise a `FileNotFoundError`

#### Scenario: Prompt directory configurable

- **WHEN** `ai.prompt_dir` is set in configuration
- **THEN** the system SHALL load prompt templates from that directory instead of the default `prompts/`

### Requirement: Maximum token configuration

The system SHALL allow configuring the maximum number of output tokens per AI request.

The `AiConfig` dataclass SHALL include a `max_tokens: int = 1024` field.

Each provider SHALL pass `max_tokens` to the underlying API/SDK call when generating text.

#### Scenario: Max tokens passed to provider

- **WHEN** a provider's `generate()` is called
- **THEN** the underlying API call SHALL include a `max_tokens` parameter matching the configured value

### Requirement: Retry logic for transient failures

The system SHALL retry failed AI provider calls on transient errors (network timeouts, 5xx HTTP status codes, service unavailability).

Retry behavior SHALL be:
- Maximum 3 retry attempts
- Exponential backoff with base delay of 1 second (1s, 2s, 4s)
- Jitter added to each delay (±250ms) to avoid thundering herd

Non-transient errors (400 Bad Request, 401 Unauthorized, invalid API key) SHALL NOT be retried.

The retry logic SHALL live in the infrastructure layer, wrapping the provider call, not in the domain or application layers.

#### Scenario: Transient failure retried

- **WHEN** `generate()` raises a `TimeoutError`
- **THEN** the system SHALL retry up to 3 times with exponential backoff

#### Scenario: Non-transient error not retried

- **WHEN** the provider returns a 401 Unauthorized status
- **THEN** the system SHALL NOT retry
- **AND** SHALL propagate the error immediately

#### Scenario: All retries exhausted

- **WHEN** all 3 retry attempts fail
- **THEN** the system SHALL raise the last exception to the caller

### Requirement: AI-specific logging

The system SHALL emit structured log entries for all AI operations to enable observability without exposing sensitive data.

A correlation ID SHALL be generated at the start of each report generation run using `uuid.uuid4().hex[:12]` and passed to all AI operations within that run. Every log entry SHALL include this correlation ID.

The following events SHALL be logged at the application layer:
- AI use case started (with report project key, finding count, correlation ID)
- AI provider call initiated (with provider name, model, prompt token count estimate)
- AI provider response received (with response time in milliseconds, response token count)
- AI response parsed successfully or failed to parse
- AI use case completed or failed
- AI disabled — skipped

Log messages SHALL NOT include:
- Full prompt text
- Full LLM response text
- API keys or tokens

#### Scenario: AI use case logs start and completion

- **WHEN** an AI use case executes
- **THEN** a log entry SHALL be emitted at the start with project key, finding count, and correlation ID
- **AND** a log entry SHALL be emitted at completion with duration

#### Scenario: Sensitive data excluded from logs

- **WHEN** any AI log entry is inspected
- **THEN** it SHALL NOT contain the full prompt, full response, or any API keys
- **AND** SHALL include the correlation ID

### Requirement: Provider health check

The system SHALL provide a mechanism to verify that a configured AI provider is reachable and authenticated before the first use.

The `AIProvider` interface SHALL include a concrete `health()` method that returns `HealthStatus()`. Provider implementations SHALL override `health()` to perform real connectivity checks.

The health check SHALL be invoked during application bootstrap when AI is enabled. If the health check fails, the system SHALL log a warning and continue in degraded mode (AI disabled for that session).

#### Scenario: Health check passed

- **WHEN** AI is enabled at startup
- **AND** the provider health check succeeds
- **THEN** the application SHALL proceed with AI enabled

#### Scenario: Health check fails gracefully

- **WHEN** AI is enabled at startup
- **AND** the provider health check fails
- **THEN** the system SHALL log the failure
- **AND** disable AI for the session
- **AND** continue report generation without AI

### Requirement: Capability registry for future extensibility

The system SHALL define a `AICapability` registry that allows new AI features to be added without modifying existing code.

A `AICapability` SHALL be defined by:
- `id: str` — unique identifier (e.g., `"executive_summary"`, `"story_quality"`, `"ac_generation"`)
- `name: str` — human-readable name
- `prompt_template: str` — prompt template filename
- `output_schema: type` — the expected output type (subclass of `AICapabilityOutput`)

The system SHALL define an `AICapabilityOutput` base dataclass in the application layer:

```python
@dataclass
class AICapabilityOutput:
    """Base class for all AI capability outputs."""
```

The `AIReviewEngine` SHALL maintain a registry of capabilities and route each capability's request to the appropriate prompt and output parser.

New capabilities SHALL be registered at composition root by adding them to the registry. No domain or application code changes SHALL be required to add a new capability.

#### Scenario: Capability registered and executed

- **WHEN** a capability with id `"executive_summary"` is registered
- **AND** the engine executes it
- **THEN** the engine SHALL load the matching prompt template
- **AND** SHALL parse the response into the registered output schema type

#### Scenario: New capability added via registration

- **WHEN** a new capability is registered at composition root
- **AND** its prompt template file exists
- **AND** its output schema is defined
- **THEN** the engine SHALL support it without any code modification in domain or application layers

### Requirement: Rate limiting

The system SHALL prevent exceeding the AI provider's API rate limits by implementing a client-side rate limiter.

The system SHALL define a `RateLimitExceeded` exception in the infrastructure layer:

```python
class RateLimitExceeded(Exception):
    """Raised when the rate limit queue is full."""
```

The rate limiter SHALL:
- Limit to a configurable number of requests per minute (`ai.rate_limit_rpm: int = 30`)
- Queue requests that exceed the limit and dispatch them as capacity becomes available
- Raise a `RateLimitExceeded` error if the queue exceeds a configurable max queue size (`ai.rate_limit_queue: int = 10`)

Rate limiting SHALL live in the infrastructure layer, wrapping provider calls.

#### Scenario: Requests within rate limit pass through

- **WHEN** requests are made at 10 requests per minute
- **AND** the rate limit is 30 RPM
- **THEN** all requests SHALL pass through without delay

#### Scenario: Rate limit exceeded — request queued

- **WHEN** requests exceed 30 RPM
- **THEN** excess requests SHALL be queued
- **AND** SHALL execute when the next window permits

#### Scenario: Queue full — request rejected

- **WHEN** the queue exceeds `rate_limit_queue` size
- **THEN** the system SHALL raise a `RateLimitExceeded` error

### Requirement: Output validation against schema

The system SHALL validate every AI provider response against a defined schema before returning it to the caller.

The system SHALL define a `SchemaValidationError` exception in the application layer:

```python
class SchemaValidationError(ValueError):
    """Raised when AI output doesn't match expected schema."""
```

Each `AICapability` SHALL define its expected output schema using Python dataclasses. The validation layer SHALL:
- Parse the LLM JSON response
- Verify all required fields are present
- Verify field types match expectations
- Raise a `SchemaValidationError` with details on what failed if validation fails

Validation SHALL occur in the application layer, after the raw response is received but before it is returned to the use case.

#### Scenario: Valid response passes validation

- **WHEN** the LLM returns a JSON matching the expected schema
- **THEN** it SHALL be parsed into the target dataclass
- **AND** returned successfully

#### Scenario: Missing field fails validation

- **WHEN** the LLM returns JSON missing the `critical_findings` field
- **THEN** a `SchemaValidationError` SHALL be raised
- **AND** the error message SHALL indicate which field is missing

#### Scenario: Wrong type fails validation

- **WHEN** the LLM returns JSON where `priority_actions` is a string instead of a list
- **THEN** a `SchemaValidationError` SHALL be raised

### Requirement: Temperature configuration per capability

The system SHALL allow configuring the LLM temperature parameter per capability to control creativity vs. determinism.

The `AiConfig` SHALL support a `capabilities` section that maps capability IDs to their settings:

```yaml
ai:
  capabilities:
    executive_summary:
      temperature: 0.3
      max_tokens: 1024
    story_quality:
      temperature: 0.5
      max_tokens: 2048
```

If a capability has no explicit configuration, the system SHALL use global defaults (`temperature: 0.3`, `max_tokens: 1024`).

#### Scenario: Capability-specific temperature used

- **WHEN** a capability has `temperature: 0.5` configured
- **THEN** the provider SHALL use `temperature=0.5` for that capability's prompts

#### Scenario: Fallback to global defaults

- **WHEN** a capability has no explicit configuration
- **THEN** the system SHALL use the global default temperature of `0.3`

### Requirement: Multiple AI models per provider

The system SHALL allow different capabilities to use different models within the same provider.

If a capability specifies a `model` override in its configuration, the system SHALL use that model for that capability instead of the provider-level default.

#### Scenario: Capability overrides model

- **WHEN** the `executive_summary` capability config specifies `model: gpt-4`
- **AND** the provider-level model is `gpt-4o-mini`
- **THEN** calls for `executive_summary` SHALL use `gpt-4`
- **AND** calls for other capabilities SHALL use `gpt-4o-mini`

### Requirement: Graceful degradation cascade

When AI is enabled but encounters failures, the system SHALL follow a defined degradation cascade:

1. If the provider fails to initialize → log warning, disable AI, continue without AI
2. If a provider call times out → retry up to 3 times with backoff
3. If all retries fail → log error, return `None` for that capability's output (not a hard failure)
4. If output validation fails → log error, return `None` for that capability's output
5. If rate limited and queue full → log warning, return `None` for that capability's output

No single AI failure SHALL block the overall report generation or raise an unhandled exception to the CLI or dashboard user.

#### Scenario: All failure modes are non-blocking

- **WHEN** an AI capability fails at any stage
- **THEN** report generation SHALL complete
- **AND** the dashboard SHALL render without that capability's output
- **AND** the error SHALL be logged with a correlation ID for debugging

### Requirement: Future capability — story quality review

The system SHALL be prepared to support a "Story Quality" capability that analyzes individual story issues for quality criteria.

This capability SHALL NOT be implemented in the current change. Only the extensibility hooks (capability registry, prompt template loading, output schema) SHALL be designed to support it.

The expected interface for this future capability is:
- Prompt template: `story_quality.txt`
- Input: Individual `Issue` domain entity fields (summary, description, acceptance criteria, story points)
- Output: `StoryQualityReview` with scores for clarity, completeness, testability

#### Scenario: Story quality hook exists in registry

- **WHEN** inspecting the capability registry
- **THEN** the registry SHALL accept a capability with id `"story_quality"` without any special handling

### Requirement: Future capability — acceptance criteria generation

The system SHALL be prepared to support an "Acceptance Criteria Generation" capability that suggests acceptance criteria for stories that lack them.

This capability SHALL NOT be implemented in the current change.

The expected interface for this future capability is:
- Prompt template: `ac_generation.txt`
- Input: Story summary and description
- Output: `GeneratedAcceptanceCriteria` with a list of suggested criteria items

### Requirement: Future capability — backlog prioritization

The system SHALL be prepared to support a "Backlog Prioritization" capability that suggests priority ordering based on findings, dependencies, and story quality.

This capability SHALL NOT be implemented in the current change.
