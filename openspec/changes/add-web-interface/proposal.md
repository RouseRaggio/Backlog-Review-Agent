# Proposal: Add Web Interface to Backlog Review Agent

## Problem Statement
Currently, the Backlog Review Agent can only be executed via the Command Line Interface (CLI), generating a static HTML report file on the local filesystem. Users (such as Product Owners, QA Engineers, and Engineering Leads) require an interactive web dashboard where they can trigger backlog audits on demand, monitor real-time execution, view quality scores and metrics, filter findings dynamically (by status, severity, and rule), and inspect individual finding details without having to run shell commands or manually open static HTML files.

## Proposed Solution
Introduce a web presentation layer consisting of:
1. A **FastAPI Presentation API** (`src/presentation/api/`) that exposes a `POST /api/reviews` endpoint. This layer reuses the existing Clean Architecture use case (`AuditBacklogUseCase`) via dependency injection, transforming domain models into explicit presentation DTOs without leaking internal entities or Jira credentials to the client.
2. A **React + TypeScript Frontend Dashboard** (`apps/backlog-review-agent/frontend/`) built with Vite and Tailwind CSS. The dashboard allows users to submit project keys and max issue limits, displays key metrics (Backlog Quality Score, Total Issues, Total Findings, PASS/FAIL/WARNING/BLOCKED breakdown), and provides an interactive, filterable findings table with detailed inspection capabilities.

## Assumptions & Boundaries
- The existing CLI workflow (`main.py` -> `parse_arguments` -> `execute` -> `HtmlReportGenerator`) remains functional and unaffected.
- Jira credentials (`JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`) remain securely on the backend server and are never sent to or requested from the frontend.
- `total_issues` represents the count of distinct Jira issue keys audited, whereas `total_findings` represents the sum of all rule evaluation findings across those issues.
- The web frontend communicates solely with the local FastAPI backend.

## Success Criteria
- User can trigger a backlog audit from the React UI by entering a Jira project key and max results.
- `POST /api/reviews` executes `AuditBacklogUseCase.execute()` and returns structured JSON with project info, BQS, statistics, and findings list.
- React dashboard accurately displays the Backlog Quality Score (BQS), total issues count, total findings count, and status breakdown cards.
- Findings table supports filtering by Status, Severity, Rule, and search by Issue Key.
- Selecting a finding shows its complete detail (Rule ID, Rule Name, Issue, Status, Severity, Message, Recommendation).
- Automated tests cover API endpoints, input validation, Jira error handling, and DTO mappings.
