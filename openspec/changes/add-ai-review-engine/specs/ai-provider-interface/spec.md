## ADDED Requirements

### Requirement: AIProvider interface contract

The system SHALL define an abstract `AIProvider` interface in the domain layer that all LLM providers must implement.

The interface SHALL define:
- A `generate(prompt: str, model: str | None = None, **kwargs) -> str` method that sends a prompt to the LLM and returns the text response.
- A `default_model` property that returns the provider's default model identifier as a string.

The interface SHALL NOT depend on any AI SDK types, HTTP libraries, or infrastructure concerns.

#### Scenario: AIProvider is defined as a Python ABC

- **WHEN** the `AIProvider` class is inspected
- **THEN** it SHALL be an abstract base class in `src/domain/`
- **AND** `generate` SHALL be decorated with `@abstractmethod`
- **AND** `default_model` SHALL be an abstract property

#### Scenario: Domain layer has no SDK imports

- **WHEN** scanning all imports in `src/domain/`
- **THEN** there SHALL be no imports from `openai`, `anthropic`, `httpx`, or any LLM SDK

### Requirement: OpenAI provider adapter

The system SHALL provide an `OpenAIProvider` class that implements `AIProvider` using the `openai` Python SDK.

The constructor SHALL accept:
- `api_key: str` — the OpenAI API key
- `model: str | None` — overrides the default model (`gpt-4o-mini`)
- `organization: str | None` — optional organization ID

`generate()` SHALL call the Chat Completions endpoint.

#### Scenario: OpenAIProvider generates text successfully

- **WHEN** `OpenAIProvider.generate("Summarize this: ...")` is called
- **THEN** it SHALL return a non-empty string

#### Scenario: OpenAIProvider uses configured model

- **WHEN** `OpenAIProvider` is constructed with `model="gpt-4"` 
- **AND** `generate()` is called
- **THEN** the API call SHALL use `model="gpt-4"`

#### Scenario: OpenAIProvider raises on missing API key

- **WHEN** `OpenAIProvider(api_key="")` is constructed
- **THEN** it SHALL raise a `ValueError`

### Requirement: Anthropic provider adapter

The system SHALL provide an `AnthropicProvider` class that implements `AIProvider` using the `anthropic` Python SDK.

The constructor SHALL accept:
- `api_key: str` — the Anthropic API key
- `model: str | None` — overrides the default model (`claude-3-haiku-20240307`)

`generate()` SHALL call the Messages API.

#### Scenario: AnthropicProvider generates text successfully

- **WHEN** `AnthropicProvider.generate("Analyze this: ...")` is called
- **THEN** it SHALL return a non-empty string

#### Scenario: AnthropicProvider raises on missing API key

- **WHEN** `AnthropicProvider(api_key="")` is constructed
- **THEN** it SHALL raise a `ValueError`

### Requirement: Ollama provider adapter

The system SHALL provide an `OllamaProvider` class that implements `AIProvider` using direct HTTP calls (no Ollama SDK dependency).

The constructor SHALL accept:
- `base_url: str` — defaults to `http://localhost:11434`
- `model: str | None` — overrides the default model (`llama3`)

`generate()` SHALL send a POST request to `{base_url}/api/generate`.

#### Scenario: OllamaProvider generates text successfully

- **WHEN** `OllamaProvider.generate("Summarize: ...")` is called
- **THEN** it SHALL return a non-empty string

#### Scenario: OllamaProvider raises on connection failure

- **WHEN** `OllamaProvider(base_url="http://localhost:19999")` is constructed
- **AND** `generate()` is called
- **THEN** it SHALL raise a `ConnectionError`

### Requirement: Provider factory

The system SHALL provide a factory function or class that creates the appropriate `AIProvider` instance based on a provider name string.

The factory SHALL accept:
- `provider_name: str` — one of `"openai"`, `"anthropic"`, `"ollama"`
- `config: dict` — provider-specific configuration

The factory SHALL raise a `ValueError` for unknown provider names.

#### Scenario: Factory creates OpenAIProvider

- **WHEN** the factory is called with `provider_name="openai"`
- **THEN** it SHALL return an instance of `OpenAIProvider`

#### Scenario: Factory raises for unknown provider

- **WHEN** the factory is called with `provider_name="unknown"`
- **THEN** it SHALL raise a `ValueError`

### Requirement: Provider timeout

All provider implementations SHALL support a configurable timeout (default 30 seconds).

If the LLM call exceeds the timeout, `generate()` SHALL raise a `TimeoutError`.

#### Scenario: Timeout is configurable

- **WHEN** any provider is constructed with `timeout=60`
- **THEN** the underlying HTTP/SDK call SHALL use a 60-second timeout

### Requirement: HealthStatus type

The system SHALL define a `HealthStatus` dataclass in the domain layer that represents the result of a provider connectivity check.

The dataclass SHALL contain:
- `reachable: bool` — whether the provider endpoint is reachable
- `auth_valid: bool` — whether the API key or credentials are valid
- `model_accessible: bool` — whether the configured model is accessible

All fields SHALL default to `False`.

#### Scenario: HealthStatus can be constructed

- **WHEN** a `HealthStatus` is created with `reachable=True`, `auth_valid=True`, `model_accessible=True`
- **THEN** all three fields SHALL be `True`

### Requirement: Provider health check method

The `AIProvider` SHALL define a `health() -> HealthStatus` method as a concrete (non-abstract) method that returns `HealthStatus()` by default.

Provider implementations SHALL override `health()` to perform real connectivity and authentication checks.

`OpenAIProvider.health()` SHALL send a lightweight request to the List Models endpoint and return the appropriate `HealthStatus`.

`AnthropicProvider.health()` SHALL send a ping to the Messages API with `max_tokens=1` and return `HealthStatus`.

`OllamaProvider.health()` SHALL send a GET request to `{base_url}/api/tags` and return `HealthStatus`.

#### Scenario: Default health() returns unreachable

- **WHEN** `AIProvider.health()` is called on a mock that does not override it
- **THEN** it SHALL return `HealthStatus(reachable=False, auth_valid=False, model_accessible=False)`

#### Scenario: OpenAI health check succeeds

- **WHEN** the List Models endpoint returns 200
- **THEN** `OpenAIProvider.health()` SHALL return `HealthStatus(reachable=True, auth_valid=True, model_accessible=True)`

#### Scenario: Ollama health check fails

- **WHEN** the Ollama server is not running
- **THEN** `OllamaProvider.health()` SHALL return `HealthStatus(reachable=False, auth_valid=False, model_accessible=False)`
