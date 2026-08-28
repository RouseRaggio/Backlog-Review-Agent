# Delta Spec: Unified UI and Navigation

## ADDED Requirements

### Requirement: Persistent Sidebar Navigation
The application SHALL render a persistent dark sidebar providing seamless switching between the ecosystem modules with active indicators and "Próximamente" badges for unreleased modules.

#### Scenario: Switching Between Modules
- **GIVEN** the user is viewing the platform
- **WHEN** the user clicks "Backlog" in the sidebar
- **THEN** the route switches to `/backlog` and the Backlog Review Agent interface is rendered
- **WHEN** the user clicks "Test Cases" in the sidebar
- **THEN** the route switches to `/test-cases` and the Test Case Generator interface is rendered.

#### Scenario: Viewing Unreleased Modules
- **GIVEN** the sidebar displays unreleased agents (`Test Data`, `Ejecución`, `Resultados`, `Bugs`, `Configuración`)
- **WHEN** the user clicks on any unreleased item
- **THEN** an informational placeholder view is displayed explaining that the module will be available in upcoming releases without generating fake actions.
