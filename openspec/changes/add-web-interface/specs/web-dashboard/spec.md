# Delta Spec: Web Dashboard for Backlog Review Agent

## ADDED Requirements

### Requirement: Interactive Review Submission
The dashboard SHALL provide input fields for Jira Project Key and Max Issues with a submission button that initiates the audit and displays a loading state.

#### Scenario: Submitting a valid review
- **GIVEN** a user enters a valid Jira project key and clicks "Iniciar revisión"
- **WHEN** the request is sent to `POST /api/reviews`
- **THEN** the dashboard displays a loading indicator and disables duplicate submissions until complete.

### Requirement: Quality Metrics and Findings Display
The dashboard SHALL render the Backlog Quality Score gauge, summary statistics cards, and a filterable table of findings with inspection modal.

#### Scenario: Displaying audit results and filtering findings
- **GIVEN** a successful review response
- **WHEN** the data is loaded into the dashboard
- **THEN** the Backlog Quality Score (BQS), Total Issues, Total Findings, and status breakdown cards are shown
- **AND** the user can filter findings by status, severity, rule, or search by issue key.
