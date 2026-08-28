# Design: Docker Architecture for Backlog Review Agent

## Architectural Overview

```text
                     Browser / Host Client
                              │
               ┌──────────────┴──────────────┐
               │  http://localhost:5173      │  http://localhost:8000
               ▼                             ▼
    ┌──────────────────────────────────────────────────┐
    │               Frontend Container                 │
    │                 (nginx:alpine)                   │
    │  Port 80 (exposed as 5173 on host)               │
    │                                                  │
    │  /           →  React Static SPA                 │
    │  /api/       →  Proxy to http://backend:8000/api/│
    │  /health     →  Proxy to http://backend:8000/health
    └────────────────────────┬─────────────────────────┘
                             │ Docker Network: backlog-network
                             ▼
    ┌──────────────────────────────────────────────────┐
    │               Backend Container                  │
    │            (python:3.11-slim non-root)           │
    │  Port 8000 (exposed as 8000 on host)             │
    │                                                  │
    │  FastAPI / Uvicorn (:8000)                       │
    │  - Environment: JIRA_URL, JIRA_EMAIL, JIRA_TOKEN │
    │  - Health Check: GET /health                    │
    │  - Bound Volume: ./reports -> /app/reports       │
    └────────────────────────┬─────────────────────────┘
                             │
                             ▼
                    Jira Cloud REST API v3
```

## Container Specifications

### 1. Backend Service
- **Build Context**: `apps/backlog-review-agent/`
- **Dockerfile**:
  - Base: `python:3.11-slim`
  - User: `appuser` (created with UID/GID 1000, non-root)
  - Workdir: `/app`
  - Dependencies: Installed via `pip install --no-cache-dir -r requirements.txt`
  - Healthcheck: Runs Python script `urllib.request.urlopen("http://localhost:8000/health")` every 10s.
  - Entrypoint: `uvicorn src.presentation.api.app:app --host 0.0.0.0 --port 8000`

### 2. Frontend Service
- **Build Context**: `apps/backlog-review-agent/frontend/`
- **Dockerfile (Multi-Stage)**:
  - **Stage 1 (`builder`)**: `node:20-alpine`, installs packages with `npm install` and executes `npm run build`.
  - **Stage 2 (`runtime`)**: `nginx:alpine`, copies `/dist` artifacts to `/usr/share/nginx/html`, copies `nginx.conf` to `/etc/nginx/conf.d/default.conf`.
- **Nginx Configuration (`nginx.conf`)**:
  - Serves static assets with SPA fallback (`try_files $uri $uri/ /index.html;`).
  - Proxies `/api/` requests to `http://backend:8000/api/` with proper proxy headers (`Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`).
  - Proxies `/health` to `http://backend:8000/health`.

### 3. Docker Compose Orchestration (`docker-compose.yml`)
- Service `backend`:
  - Builds from `.`
  - Port mapping: `8000:8000`
  - Network: `backlog-network`
  - Volume: `./reports:/app/reports`
  - Environment: Inherits `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `CORS_ORIGINS` from `.env`
  - Healthcheck: Defined with 10s interval, 5s timeout, 3 retries
- Service `frontend`:
  - Builds from `./frontend`
  - Port mapping: `5173:80`
  - Network: `backlog-network`
  - `depends_on`: Waits for `backend` condition `service_healthy`
- Network: `backlog-network` bridge driver.

## Security & Isolation
- No credentials or `.env` files are baked into any image.
- Both backend and frontend build contexts use dedicated `.dockerignore` files to prevent uploading `.env`, `.git`, `.venv`, `__pycache__`, or `node_modules`.
- Root `.gitignore` prevents committing `.env` files.
- Non-root user in the Python container reduces privilege escalation risk.
