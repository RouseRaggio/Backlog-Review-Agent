# Proposal: Unified QA Automation Platform Frontend

## Problem Statement
The `AI-QA-Agents` ecosystem currently features two independent agents with their own isolated frontends running on different ports (`5173` for Backlog Review Agent, `5174` for Test Case Generator Agent). As additional agents join the ecosystem (Test Data Generator, Execution Agent, Result Analysis Agent, Bug Creation Agent), running individual web UIs causes fragmented user experience and friction when transitioning data between stages (e.g. manually copy-pasting User Stories from Backlog Review into Test Case Generator).

## Proposed Solution
Create a single, unified frontend Single Page Application (SPA) in `apps/qa-platform/` running on port `5175`.
- **Unified Navigation & Layout**: A permanent, polished Dark UI sidebar providing immediate access to the `/` (Dashboard with live agent health status), `/backlog` (Backlog Review module), `/test-cases` (Test Case Generator module), and placeholder views for future agents (`/test-data`, `/execution`, `/results`, `/bugs`, `/configuration`).
- **Zero Backend Coupling**: The agents remain completely separate Clean Architecture microservices on ports `8000` and `8001`.
- **Seamless Inter-Agent Workflow**: Direct action in the Backlog view allowing users to click *"🧪 Generar Test Cases"* on an audited issue, automatically transferring its story and criteria to the Test Case Generator module without manual copy-pasting.

## Success Criteria
1. Single unified UI accessible at `http://localhost:5175`.
2. Backlog Review and Test Case Generator modules consume their respective APIs (`8000` and `8001`) with full feature parity.
3. Live healthcheck querying in Dashboard shows real-time Online/Offline statuses.
4. Seamless transfer of story and criteria from Backlog into Test Cases.
5. Existing standalone frontends (`5173`, `5174`) and backend test suites remain completely operational.
