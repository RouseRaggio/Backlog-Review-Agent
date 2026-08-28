# Delta Spec: QA Platform Web Application

## ADDED Requirements

### Requirement: Unified Platform Portal
The QA Platform SHALL provide a unified single-page web interface serving as the central cockpit for all AI-QA agents in the ecosystem.

#### Scenario: Navigating to the Platform Root
- **GIVEN** the QA Platform is running on port 5175
- **WHEN** a user visits `http://localhost:5175/`
- **THEN** the Dashboard view is displayed showing ecosystem overview and live agent health status badges.

#### Scenario: Querying Agent Health Status
- **GIVEN** the Dashboard is active
- **WHEN** the platform queries the health endpoints (`GET :8000/health` and `GET :8001/health`)
- **THEN** the respective agent cards display "Online" in green when healthy or "Offline" in red when unreachable without breaking the UI.
