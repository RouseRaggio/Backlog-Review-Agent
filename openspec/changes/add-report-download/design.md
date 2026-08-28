# Design: HTML Report Download for Backlog Review Agent

## Architectural Context
The HTML report download capability connects the existing `HtmlReportGenerator` presentation adapter with the FastAPI presentation API and React frontend dashboard.

```text
React Dashboard (App.tsx)
        │
        │ 1. POST /api/reviews
        ▼
FastAPI Routes (create_review)
   ├── AuditBacklogUseCase.execute()  ──► Domain Evaluation
   └── HtmlReportGenerator.generate() ──► Writes reports/latest/{PROJECT}_AUDIT.html
        │
        │ 2. GET /api/reviews/{project_key}/report
        ▼
FastAPI Routes (download_review_report)
   ├── Strict regex validation on project_key
   ├── Path traversal verification: resolved_path.is_relative_to(reports_dir)
   └── Returns FileResponse(media_type="text/html", filename="{PROJECT}_AUDIT.html")
        │
        ▼
Browser downloads {PROJECT}_AUDIT.html via Blob URL
```

## Detailed Specifications

### 1. API Route Implementation
- Endpoint: `GET /api/reviews/{project_key}/report`
- Input: `project_key: str` path parameter.
- Validation:
  - Pattern: `^[A-Za-z0-9_-]+$` (only alphanumeric, hyphens, and underscores allowed).
  - Traversal defense: Explicit check verifying that the resolved path is located within `reports/latest/`.
- Behavior:
  - If valid and file exists: Returns `FileResponse` with `media_type="text/html"` and attachment header.
  - If file does not exist: Returns HTTP 404 with error detail `Reporte no encontrado para el proyecto '{project_key}'`.
  - If invalid identifier: Returns HTTP 400 with error detail `Clave de proyecto inválida`.

### 2. Frontend Client & UI
- Service: `downloadReport(projectKey: string): Promise<void>` in `src/services/api.ts`.
- Component integration:
  - Button located in the project overview banner in `App.tsx`.
  - Loading state disables duplicate clicks and renders a spinner (`Loader2`).
  - Success message ("Reporte descargado") auto-resets after 3 seconds.
  - Error state informs the user without interrupting dashboard interaction.

### 3. Storage and Docker Persistence
- The report files remain in `reports/latest/{PROJECT}_AUDIT.html`, mapped to the host via the Docker volume `./reports:/app/reports`.
