# Delta Spec: Test Case Generator Dashboard

## ADDED Requirements

### Requirement: Interactive Test Case Generation UI
The web dashboard SHALL render an interactive QA-oriented dark UI allowing users to input a User Story, manage dynamic Acceptance Criteria, configure generation options, and trigger test case synthesis.

#### Scenario: Submitting Generation Request
- **GIVEN** a user enters a User Story and multiple Acceptance Criteria in the dashboard
- **WHEN** the user clicks "Generar Test Cases"
- **THEN** the interface displays a loading state
- **AND** renders the generated test cases, traceability metrics, and summary breakdown cards upon completion.

### Requirement: Test Cases Table, Filtering, and Inspection
The dashboard SHALL provide a filterable table of generated test cases and a modal to view complete test details.

#### Scenario: Inspecting and Filtering Test Cases
- **GIVEN** a list of generated test cases in the table
- **WHEN** the user filters by type, priority, or searches by title/ID
- **THEN** the table displays matching cases
- **AND** selecting a row opens a detail view with steps, preconditions, required data, expected result, and traceability references.
