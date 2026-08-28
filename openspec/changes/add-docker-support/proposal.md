# Proposal: Add Docker Support to Backlog Review Agent

## Problem Statement
The Backlog Review Agent comprises a Python FastAPI backend and a React TypeScript frontend. Running the system previously required manual local environment setup (Python 3.11+, Node 20+, installing pip packages, npm dependencies, managing environment variables, and starting both processes independently). To simplify deployment, ensure reproducible environments across machines, and maintain secure credential isolation, the agent needs a complete Docker Compose solution.

## Proposed Solution
Provide a multi-container Docker setup:
1. **Backend Container (`python:3.11-slim`)**: Runs FastAPI with Uvicorn on port 8000 under a dedicated non-root user (`appuser`). Uses health check monitoring via `GET /health` and mounts `./reports:/app/reports` to preserve generated HTML audit reports.
2. **Frontend Container (`node:20-alpine` -> `nginx:alpine`)**: Multi-stage build producing a lightweight Nginx image listening on port 80 (mapped to host 5173). Serves Vite-built static assets and acts as a reverse proxy for `/api/` requests to `http://backend:8000/api/`.
3. **Docker Compose (`docker-compose.yml`)**: Coordinates both services on an internal bridge network (`backlog-network`), loads runtime credentials from `.env`, and ensures the frontend waits for the backend to be healthy before accepting traffic.

## Assumptions & Boundaries
- Jira credentials (`JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`) remain outside of images, loaded solely at runtime via environment variables / `.env`.
- Clean Architecture layers, Domain rules, Score calculation, and CLI execution remain unchanged.
- The browser accesses the UI at `http://localhost:5173` and the API directly at `http://localhost:8000` or proxied via `http://localhost:5173/api/`.

## Success Criteria
- `docker compose up --build` builds and starts both containers cleanly.
- `GET http://localhost:8000/health` and `GET http://localhost:5173/health` respond with HTTP 200.
- React frontend loads at `http://localhost:5173` and communicates with the backend via relative `/api` paths.
- Reports generated inside the container persist on host `./reports/latest/`.
- No credentials or `.env` files are included in images or version control.
