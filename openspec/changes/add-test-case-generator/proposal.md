# Proposal: Add Test Case Generator Agent

## Problem Statement
Writing structured, complete, and fully traceable test cases from User Stories and Acceptance Criteria is time-consuming and often subject to human omissions or unwarranted assumptions. Within the `AI-QA-Agents` ecosystem, there is a need for a dedicated, independent agent—the **Test Case Generator Agent**—that analyzes User Stories and explicit Acceptance Criteria to generate structured positive, negative, validation, and boundary test cases.

## Core Principle: No Invention (Strict Grounding)
The primary quality criterion of this agent is:
> *"Es preferible generar menos casos de prueba correctamente trazables que generar muchos casos basados en supuestos."*

The generator strictly differentiates between:
- **Known / Explicit Information**: Clauses directly stated in the User Story and Acceptance Criteria.
- **Unknown / Unspecified Information**: Omissions regarding format, field lengths, regex rules, domain restrictions, or boundary thresholds.

The agent **never** invents business rules or unmentioned constraints. When boundary conditions or criteria are missing, it issues an explicit warning and adjusts the confidence level rather than generating speculative test cases.

## Proposed Solution
Introduce `apps/test-case-generator-agent/` as an independent module with:
1. **Clean Architecture Core (Domain & Application)**:
   - Entities: `UserStory`, `AcceptanceCriterion`, `TestCase`, `GenerationResult`.
   - Use Case: `GenerateTestCasesUseCase`.
   - Ports: `TestCaseGenerator` interface with initial `RuleBasedTestCaseGenerator` (rule-based deterministic parser) and prepared stub for future `LLMTestCaseGenerator`.
2. **FastAPI Presentation Layer**:
   - `POST /api/test-cases/generate` returning structured DTOs with test cases, metrics, warnings, and traceability map.
   - `GET /health` endpoint for readiness checking.
3. **React + TypeScript Dashboard**:
   - Dark UI with sidebar navigation (Test Cases active, future modules marked as "Próximamente").
   - Dynamic Acceptance Criteria editor, generation options, and interactive results table with search, multi-facet filtering, detail modal, clipboard copying, and JSON export.
4. **Dockerization**:
   - Docker Compose running backend on `8001:8000` and frontend on `5174:80` on isolated network `test-case-generator-network`.

## Success Criteria
- Given a User Story and Acceptance Criteria, the agent generates traceable positive, negative, and validation test cases strictly supported by the text.
- Boundary cases are generated **only** if explicit limits, ranges, or thresholds are provided.
- If no criteria are supplied or boundary info is missing, clear warnings are reported and confidence is appropriately degraded.
- Independent tests and Docker containers operate without any conflict with Backlog Review Agent.
