# Delta Spec: Test Case Generation Logic

## ADDED Requirements

### Requirement: Evidence-Based Test Case Generation
The system SHALL generate test cases derived strictly from explicit statements in the User Story and Acceptance Criteria without hallucinating business constraints or unmentioned rules.

#### Scenario: Generating Positive Test Cases from Explicit Capabilities
- **GIVEN** an acceptance criterion stating "El administrador puede crear un usuario proporcionando nombre, correo electrónico y rol"
- **WHEN** the generation use case is executed
- **THEN** a positive test case is generated with steps and expected results covering creation with valid name, email, and role
- **AND** `acceptance_criteria_reference` is set to the corresponding criterion ID
- **AND** `confidence` is set to HIGH.

#### Scenario: Generating Negative Test Cases from Explicit Uniqueness Rules
- **GIVEN** an acceptance criterion stating "El sistema valida que el correo electrónico sea único"
- **WHEN** the generation use case is executed
- **THEN** a negative validation test case is generated verifying rejection of a duplicate email
- **AND** no speculative rules (such as email regex, domain whitelist, or max length) are added.

#### Scenario: Handling Missing Boundary Information
- **GIVEN** an input without any explicit numeric limits, ranges, or thresholds
- **WHEN** boundary test case generation is evaluated
- **THEN** no boundary test cases are created
- **AND** a warning is returned stating: "No se generaron casos límite porque la Historia de Usuario y los criterios de aceptación no especifican valores límite o umbrales."

#### Scenario: Generating Boundary Cases for Explicit Numerical Limits
- **GIVEN** an acceptance criterion stating "El nombre debe tener entre 3 y 50 caracteres"
- **WHEN** boundary generation is executed
- **THEN** boundary test cases covering min (3), max (50), below min (2), and above max (51) are generated with HIGH confidence.

### Requirement: Insufficient Information Detection
The system SHALL detect when no acceptance criteria are provided and adjust the confidence level.

#### Scenario: Generating from Story without Criteria
- **GIVEN** a User Story without any Acceptance Criteria
- **WHEN** the generation use case is executed
- **THEN** basic functional scenarios are generated directly from the story text
- **AND** `confidence` is marked as LOW
- **AND** `status` is marked as REVIEW_REQUIRED
- **AND** a warning is emitted stating criteria were not provided.
