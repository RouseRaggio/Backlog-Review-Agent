# Tasks: Add HTML Report Download to Backlog Review Agent

- [x] 1. Create OpenSpec proposal, design, and delta spec artifacts <!-- id: 1 -->
- [x] 2. Update `create_review` route to invoke `HtmlReportGenerator` on audit execution <!-- id: 2 -->
- [x] 3. Implement `GET /api/reviews/{project_key}/report` endpoint with security validation and `FileResponse` <!-- id: 3 -->
- [x] 4. Add comprehensive backend unit tests for report download and path traversal protection <!-- id: 4 -->
- [x] 5. Implement `downloadReport(projectKey)` in frontend API service <!-- id: 5 -->
- [x] 6. Integrate download button and state management in `App.tsx` <!-- id: 6 -->
- [x] 7. Verify frontend build and run pytest test suite <!-- id: 7 -->
- [x] 8. Validate OpenSpec change with `openspec validate add-report-download` <!-- id: 8 -->
