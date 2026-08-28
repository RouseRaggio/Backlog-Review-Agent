# Delta Spec: Jira as Primary Source for Test Case Generation

## ADDED Requirements

### Requirement: Querying Jira for User Stories
The system SHALL retrieve Jira issues by `project_key` and `issue_key`, extracting the summary, description, and metadata into a domain `UserStory` representation.

#### Scenario: Successfully Fetching an Existing Jira Story
- **GIVEN** valid Jira credentials and an existing issue key `GES-40`
- **WHEN** the analysis use case is executed
- **THEN** the system retrieves the issue summary and description from Jira
- **AND** sets the source property to "jira"
- **AND** returns HTTP 200 with the parsed User Story and extracted Acceptance Criteria.

#### Scenario: Handling Non-Existent Jira Issue
- **GIVEN** a query for a non-existent issue `NONEXIST-999`
- **WHEN** the analysis endpoint is called
- **THEN** the system returns HTTP 404 with message "Historia de Usuario no encontrada en Jira."

#### Scenario: Handling Permission or Authentication Errors
- **GIVEN** invalid Jira credentials or restricted permissions
- **WHEN** Jira responds with HTTP 401 or 403
- **THEN** the system returns HTTP 403 with message "No tienes permisos para consultar esta Issue." without exposing tokens or authorization headers.

### Requirement: Automated Acceptance Criteria Extraction
The system SHALL extract acceptance criteria from custom fields or parse structured blocks (numbered lists, bullets, Gherkin, AC tags) within the issue description.

#### Scenario: Extracting Criteria from Formatted Description
- **GIVEN** a Jira issue description containing:
  ```text
  Como administrador quiero gestionar usuarios para controlar accesos.
  Criterios de Aceptación:
  1. El administrador puede crear un usuario con nombre y rol.
  2. El sistema valida que el correo sea único.
  ```
- **WHEN** the issue is parsed
- **THEN** criteria `AC-001` and `AC-002` are extracted with their respective descriptions
- **AND** sufficiency is flagged as TRUE with confidence HIGH.

#### Scenario: Handling Issues without Acceptance Criteria
- **GIVEN** a Jira issue description with only story text and no criteria
- **WHEN** the issue is analyzed
- **THEN** an empty criteria list is returned
- **AND** a warning is emitted stating criteria were not found in Jira
- **AND** confidence is marked as LOW.

### Requirement: Backward-Compatible Manual Fallback
The system SHALL accept manually provided User Story and Acceptance Criteria payloads without querying Jira when manual data is supplied.

#### Scenario: Generating from Manual Fallback Payload
- **GIVEN** a generation request containing explicit `user_story` and `acceptance_criteria`
- **WHEN** `POST /api/test-cases/generate` is executed
- **THEN** the system generates test cases directly from the provided payload without making external calls to Jira.
