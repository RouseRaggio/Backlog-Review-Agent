# Proposal: Integrate Jira as Primary Source for Test Case Generator Agent

## Problem Statement
Currently, users of the Test Case Generator Agent must manually type or copy-paste the User Story and Acceptance Criteria into the application. Since user stories, acceptance criteria, and requirement specifications already reside within Jira, requiring manual data entry introduces friction and potential transcription mistakes.

## Proposed Solution
Upgrade the **Test Case Generator Agent** (`apps/test-case-generator-agent/`) to make **Jira the primary source of truth**:
1. **Jira REST Client & Infrastructure Adapter**:
   - Query Jira REST API (`/rest/api/3/issue/{issue_key}`) to fetch summary, description, custom fields, components, priority, and status.
   - Robust parsing of Acceptance Criteria from custom fields (`JIRA_ACCEPTANCE_CRITERIA_FIELD`) or embedded structured description blocks (Gherkin, numbered criteria, bullet lists, `AC-XXX` patterns).
2. **Analysis & Generation Endpoints**:
   - `POST /api/test-cases/analyze`: Retrieves the issue from Jira, parses the User Story and Acceptance Criteria, checks sufficiency, and returns a structured preview.
   - `POST /api/test-cases/generate`: Directly generates test cases from Jira (or from manually provided input if supplied as a fallback).
3. **Clean Architecture & No-Invention Enforcement**:
   - Domain layer remains 100% pure via a `JiraGateway` port interface.
   - Strict "NO INVENTAR" rule: If acceptance criteria are absent or boundary values are unstated, emit warnings, assign `confidence: LOW`, and mark `status: REVIEW_REQUIRED`.
4. **Interactive Jira-First Frontend with Manual Fallback**:
   - The UI requests Project and Issue Key (e.g. `GES`, `GES-40`), offers an *"🔎 Analizar Historia"* step, visualizes detected criteria, and triggers test generation.
   - A *"Modo manual"* toggle ensures users can manually enter/edit requirements if Jira is unavailable or for ad-hoc testing.
   - Reusable across both the standalone frontend (`:5174`) and the unified **QA Platform** (`:5175`).

## Success Criteria
- Given `project_key` and `issue_key`, the agent retrieves the User Story and Acceptance Criteria from Jira automatically.
- Generated Test Cases are traceable to Jira criteria without manual copy-pasting.
- Clear error handling for Jira 404, 401/403, 500, timeout, and configuration issues without secret leakage.
- 100% backward compatibility for manual input payloads.
