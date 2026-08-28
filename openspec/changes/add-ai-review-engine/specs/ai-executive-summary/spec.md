## ADDED Requirements

### Requirement: AiExecutiveSummary domain entity

The system SHALL define an `AiExecutiveSummary` domain entity that holds the structured result of an AI analysis.

The entity SHALL contain:
- `overall_assessment: str` — a 2-3 sentence summary of overall backlog quality
- `critical_findings: list[str]` — the 3-5 most important issues found
- `priority_actions: list[PriorityAction]` — recommended actions with rationale

A `PriorityAction` SHALL be a nested dataclass with:
- `action: str` — what to do
- `rationale: str` — why this action matters

#### Scenario: AiExecutiveSummary can be constructed

- **WHEN** an `AiExecutiveSummary` is created with all fields
- **THEN** it SHALL have `overall_assessment`, `critical_findings`, and `priority_actions` accessible as attributes

#### Scenario: PriorityAction is a separate dataclass

- **WHEN** a `PriorityAction` is constructed
- **THEN** it SHALL have `action` and `rationale` fields

### Requirement: AiExecutiveSummary is optional on AuditReport

The `AuditReport` entity SHALL gain an optional `ai_summary: AiExecutiveSummary | None` field, defaulting to `None`.

The field SHALL NOT affect existing serialization, scoring, or comparison logic.

#### Scenario: AuditReport with AI summary

- **WHEN** an `AuditReport` is constructed with `ai_summary=AiExecutiveSummary(...)`
- **THEN** the field SHALL be accessible as `report.ai_summary`

#### Scenario: AuditReport without AI summary

- **WHEN** an `AuditReport` is constructed with no `ai_summary`
- **THEN** `report.ai_summary` SHALL be `None`

### Requirement: GenerateExecutiveSummary use case

The system SHALL provide a `GenerateExecutiveSummary` use case in the application layer.

The constructor SHALL accept an `AIProvider` instance (injected).

`execute(report: AuditReport) -> AiExecutiveSummary` SHALL:
1. Build a structured prompt from the report data
2. Call `AIProvider.generate(prompt)`
3. Parse the LLM response as JSON
4. Return an `AiExecutiveSummary`

If the LLM response cannot be parsed as valid JSON matching the expected schema, the use case SHALL raise a `ValueError`.

#### Scenario: Successful summary generation

- **WHEN** `execute()` is called with a valid `AuditReport`
- **AND** the AI provider returns valid JSON
- **THEN** it SHALL return an `AiExecutiveSummary` with all fields populated

#### Scenario: Unparseable LLM response

- **WHEN** `execute()` is called
- **AND** the AI provider returns non-JSON text
- **THEN** it SHALL raise a `ValueError`

#### Scenario: Prompt includes project stats

- **WHEN** `execute()` is called
- **THEN** the prompt sent to the AI SHALL include: project key, total findings, PASS/FAIL/WARNING/BLOCKED counts, quality score, and top 5 failed rules

### Requirement: AI analysis runs after deterministic evaluation

The `AuditBacklogUseCase` SHALL invoke `GenerateExecutiveSummary` after all deterministic rules have been evaluated and the `AuditReport` has been assembled.

AI execution SHALL only occur when the AI configuration has `enabled: true`.

If the AI provider raises any exception, the use case SHALL log the error and continue without an AI summary (fail-open behavior).

#### Scenario: AI disabled — no summary generated

- **WHEN** `AuditBacklogUseCase.execute()` is called
- **AND** AI is disabled in configuration
- **THEN** the returned `AuditReport` SHALL have `ai_summary` set to `None`

#### Scenario: AI enabled — summary attached to report

- **WHEN** `AuditBacklogUseCase.execute()` is called
- **AND** AI is enabled
- **AND** the AI provider responds successfully
- **THEN** `report.ai_summary` SHALL contain the generated summary

#### Scenario: AI provider error — report without summary

- **WHEN** `AuditBacklogUseCase.execute()` is called
- **AND** AI is enabled
- **AND** the AI provider raises an exception
- **THEN** the use case SHALL log the error
- **AND** continue execution
- **AND** return the `AuditReport` with `ai_summary` set to `None`

### Requirement: HTML dashboard displays AI summary

The HTML report SHALL display an "AI Executive Summary" section above the charts grid.

The section SHALL:
- Be visually distinguished with a turquoise AI icon (different from existing warning/error icons)
- Show the `overall_assessment` text
- List `critical_findings` as a bullet list
- List `priority_actions` with each action and its rationale
- Be conditionally hidden when `ai_summary` is `None`

The section SHALL NOT affect the layout or visibility of any existing dashboard component.

#### Scenario: AI summary rendered when present

- **WHEN** the HTML report is generated with a non-null `ai_summary`
- **THEN** the rendered page SHALL contain an AI Executive Summary card above the charts
- **AND** it SHALL display the overall assessment, critical findings, and priority actions

#### Scenario: AI summary hidden when absent

- **WHEN** the HTML report is generated with `ai_summary` set to `None`
- **THEN** the rendered page SHALL NOT display the AI Executive Summary section

### Requirement: CLI displays AI summary

The CLI output SHALL print the AI Executive Summary when available, after the standard summary line.

The output SHALL include the overall assessment and priority actions.

#### Scenario: CLI prints AI summary

- **WHEN** a report with `ai_summary` is printed via the CLI
- **THEN** the output SHALL include the overall assessment text and top 3 priority actions
