# Delta Spec: HTML Report Download for Backlog Review Agent

## ADDED Requirements

### Requirement: Download Generated HTML Audit Report
The system SHALL expose an HTTP endpoint `GET /api/reviews/{project_key}/report` that returns the generated HTML audit report for the specified Jira project.

#### Scenario: Successful HTML Report Download
- **GIVEN** a valid and existing `project_key` (e.g. "GESTADOC") with a generated report in `reports/latest/GESTADOC_AUDIT.html`
- **WHEN** a client sends a `GET /api/reviews/GESTADOC/report` request
- **THEN** the server returns HTTP 200 with `Content-Type: text/html`
- **AND** `Content-Disposition: attachment; filename="GESTADOC_AUDIT.html"`
- **AND** the response body contains the complete HTML report content.

#### Scenario: Non-Existent Report Request
- **GIVEN** a valid `project_key` for which no audit report exists
- **WHEN** a client sends a `GET /api/reviews/{project_key}/report` request
- **THEN** the server returns HTTP 404 with detail message explaining that the report was not found.

#### Scenario: Malformed or Traversal Project Key
- **GIVEN** a `project_key` containing path traversal characters (such as `..`, `/`, `\`) or invalid characters
- **WHEN** a client sends a request to the report endpoint
- **THEN** the server returns HTTP 400 Bad Request
- **AND** prevents access to arbitrary filesystem paths.

### Requirement: Frontend Report Download Action
The web dashboard SHALL display an option to download the HTML audit report upon successful review completion.

#### Scenario: Initiating report download from dashboard
- **GIVEN** an audit has completed successfully and results are displayed in the dashboard
- **WHEN** the user clicks "Descargar reporte HTML"
- **THEN** the dashboard fetches the report Blob from `/api/reviews/{project_key}/report`
- **AND** triggers a browser file download of `{PROJECT}_AUDIT.html` without reloading the page.
