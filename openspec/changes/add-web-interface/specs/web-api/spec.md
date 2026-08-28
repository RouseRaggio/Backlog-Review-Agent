# Delta Spec: Web API for Backlog Review Agent

## ADDED Requirements

### Requirement: Trigger Backlog Review via REST API
The system SHALL expose an HTTP endpoint `POST /api/reviews` that triggers a backlog audit for a specified Jira project.

#### Scenario: Successful Backlog Audit Request
- **GIVEN** a valid `project_key` (e.g., "GESTADOC") and an optional `max_results` parameter
- **WHEN** a client sends a `POST /api/reviews` request
- **THEN** the server executes `AuditBacklogUseCase`
- **AND** returns HTTP 200 with structured JSON containing `project`, `quality_score`, `statistics`, and `findings`.

#### Scenario: Invalid Request Parameters
- **GIVEN** an empty or whitespace-only `project_key` or non-positive `max_results`
- **WHEN** a client sends a `POST /api/reviews` request
- **THEN** the server rejects the request with HTTP 422 Unprocessable Entity.

### Requirement: Distinct Metrics for Issues and Findings
The system SHALL calculate `total_issues` as the count of distinct `issue_key`s present in findings, while `total_findings` SHALL represent the sum of all rule evaluations.

#### Scenario: Aggregation of Issue and Finding Counts
- **GIVEN** multiple rule evaluations for the same issue
- **WHEN** the API formats the response DTO
- **THEN** `statistics.total_issues` reflects the unique count of issues
- **AND** `statistics.total_findings` reflects the total count of evaluated findings.
