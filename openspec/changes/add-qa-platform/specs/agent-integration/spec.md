# Delta Spec: Inter-Agent Integration

## ADDED Requirements

### Requirement: Direct Backlog-to-TestCase Workflow
The platform SHALL allow users in the Backlog Review module to select an Issue/User Story and trigger test case generation directly, transmitting the required parameters without manual copy-pasting.

#### Scenario: Triggering Test Case Generation from an Issue
- **GIVEN** the user is viewing the findings for an audited Jira issue in `/backlog`
- **WHEN** the user clicks "🧪 Generar Test Cases" on that issue
- **THEN** the platform automatically loads the `/test-cases` module
- **AND** pre-populates `project_key`, `issue_key`, `user_story`, and related criteria
- **AND** allows the user to immediately generate structured test cases.
