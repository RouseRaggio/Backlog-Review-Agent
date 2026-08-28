# Tasks: Add Jira Source to Test Case Generator Agent

- [x] 1. Create OpenSpec proposal, design, and delta spec artifacts <!-- id: 1 -->
- [x] 2. Implement Jira configuration, exceptions, and `JiraGateway` domain port <!-- id: 2 -->
- [x] 3. Implement `JiraClient` and `CriteriaExtractor` in infrastructure layer <!-- id: 3 -->
- [x] 4. Implement `AnalyzeUserStoryUseCase` and update `GenerateTestCasesUseCase` <!-- id: 4 -->
- [x] 5. Implement `POST /api/test-cases/analyze` and update `POST /api/test-cases/generate` in FastAPI <!-- id: 5 -->
- [x] 6. Write comprehensive unit tests for JiraClient, CriteriaExtractor, UseCases, and API endpoints <!-- id: 6 -->
- [x] 7. Update frontend in `apps/test-case-generator-agent/frontend/` with Jira search, preview, and manual fallback <!-- id: 7 -->
- [x] 8. Update unified `apps/qa-platform/` frontend to support the new Jira-first flow <!-- id: 8 -->
- [x] 9. Update `.env.example`, `docker-compose.yml`, and `README.md` <!-- id: 9 -->
- [x] 10. Run all test suites, verify frontend builds, and validate OpenSpec <!-- id: 10 -->
