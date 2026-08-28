# Design: QA Platform Architecture & Routing

## Architectural Context

```text
                               AI-QA AGENTS
                          QA AUTOMATION PLATFORM
                                     │
                               React SPA (Vite)
                                  Port 5175
                                     │
    ┌────────────────────────┬───────┴────────┬──────────────────────┐
    │                        │                │                      │
    ▼                        ▼                ▼                      ▼
Dashboard (/)            /backlog        /test-cases            /test-data ...
Live Health Monitor          │                │                 (Próximamente)
    │                        ▼                ▼
    │               Backlog Review API   Test Case Generator API
    │                   Port 8000            Port 8001
    │                        ▲                ▲
    └────────────────────────┴────────────────┘
```

## Modular Routing & State Management

- **Router**: Client-side SPA routing (using React state / custom hash/history router or lightweight SPA routing) with consistent layout (Sidebar + Topbar + Content Canvas).
- **Inter-Agent Context**: Shared state store / service allowing `/backlog` findings and issues to pre-fill the form in `/test-cases` and transition the view smoothly.
- **Service Layer**:
  - `src/services/backlogApi.ts`: Consumes `VITE_BACKLOG_API_URL` (`POST /api/reviews`, `GET /api/reviews/{key}/report`, `GET /health`).
  - `src/services/testCaseApi.ts`: Consumes `VITE_TEST_CASE_API_URL` (`POST /api/test-cases/generate`, `GET /health`).
- **Nginx & Docker**:
  - `Dockerfile`: Node 20 builder $\to$ Nginx alpine runtime on port 80 (mapped to `5175:80`).
  - `nginx.conf`: Single Page Application fallback (`try_files $uri $uri/ /index.html`).
