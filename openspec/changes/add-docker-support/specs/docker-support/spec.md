# Delta Spec: Docker Support for Backlog Review Agent

## ADDED Requirements

### Requirement: Multi-Container Docker Environment
The system SHALL provide a multi-container Docker Compose setup that runs the FastAPI backend and React frontend services in an isolated bridge network.

#### Scenario: Running the application stack with Docker Compose
- **GIVEN** a configured `.env` file with Jira credentials
- **WHEN** the operator executes `docker compose up --build`
- **THEN** Docker builds both backend and frontend images
- **AND** starts both containers on the `backlog-network`
- **AND** exposes the backend on host port 8000 and frontend on host port 5173.

### Requirement: Nginx Reverse Proxy and SPA Routing
The frontend container SHALL run Nginx to serve the React single-page application and reverse-proxy API calls to the backend service.

#### Scenario: Routing frontend requests to backend
- **GIVEN** the frontend and backend containers are running
- **WHEN** a client navigates to `http://localhost:5173/` or sends a request to `http://localhost:5173/api/reviews`
- **THEN** Nginx serves the React SPA for page requests
- **AND** proxies `/api/` calls to `http://backend:8000/api/` without client CORS errors.

### Requirement: Backend Health Check
The backend container SHALL provide a health check endpoint `GET /health` used by Docker Compose to determine container readiness.

#### Scenario: Backend health check probe
- **GIVEN** the backend container is running
- **WHEN** the Docker health check probes `http://localhost:8000/health`
- **THEN** the server responds with HTTP 200 `{"status": "ok", "service": "backlog-review-agent"}`
- **AND** Docker marks the container as `healthy`.

### Requirement: Secure Credential and Secret Isolation
The Docker images SHALL NOT contain any baked credentials, API tokens, or `.env` files.

#### Scenario: Building images without secrets
- **GIVEN** the Docker build process for backend and frontend
- **WHEN** the images are built from their respective contexts
- **THEN** `.dockerignore` prevents `.env` and sensitive files from entering the build context
- **AND** credentials are only supplied at container runtime via environment variables.
