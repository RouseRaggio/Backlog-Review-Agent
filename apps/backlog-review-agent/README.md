# Backlog Review Agent

## Descripción

**Backlog Review Agent** es un agente de QA especializado en la auditoría y evaluación automática de la calidad de requerimientos e historias de usuario en **Jira Cloud**.

Su objetivo es detectar problemas de completitud, ambigüedad, falta de criterios de aceptación, asignación o estimación antes de que las historias entren al proceso de desarrollo, calculando el **Backlog Quality Score (BQS)** y generando recomendaciones accionables.

Forma parte de la plataforma **AI-QA-Agents**.

---

# Arquitectura

El proyecto sigue estrictamente los principios de **Clean Architecture**, **SOLID** y **Specification Driven Development (SDD)**.

```text
                        ┌──────────────────────────────┐
                        │      PRESENTATION LAYER      │
                        │                              │
                        │  CLI:      main.py           │
                        │  HTML:     HtmlReportGen     │
                        │  REST API: FastAPI (routes)  │
                        │  Web UI:   React TypeScript  │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │      APPLICATION LAYER       │
                        │                              │
                        │     AuditBacklogUseCase      │
                        └──────────────┬───────────────┘
                                       │
                        ┌──────────────┴───────────────┐
                        ▼                              ▼
          ┌───────────────────────────┐  ┌───────────────────────────┐
          │       DOMAIN LAYER        │  │   INFRASTRUCTURE LAYER    │
          │                           │  │                           │
          │ Entities: AuditReport,    │  │ JiraClient (REST API v3)  │
          │           Finding, Issue  │  │ JiraConfig (env parsing)  │
          │ Services: RuleEngine,     │  │ JiraMapper                │
          │           ScoreService    │  │                           │
          └───────────────────────────┘  └───────────────────────────┘
```

### Estructura de Carpetas

```text
apps/backlog-review-agent/
├── config/                     # Configuraciones YAML
├── docs/                       # Documentación SDD, SRS y ADR
├── frontend/                   # Interfaz Web (React + TypeScript + Vite + Tailwind)
│   ├── src/
│   │   ├── components/         # ReviewForm, ScoreGauge, StatsCards, FindingsTable, FindingDetailModal
│   │   ├── services/           # Cliente HTTP API
│   │   ├── types/              # Interfaces TypeScript (DTOs)
│   │   ├── App.tsx             # Dashboard principal
│   │   └── main.tsx
│   ├── Dockerfile              # Multi-stage build (Node -> Nginx)
│   ├── nginx.conf              # Reverse proxy /api/ -> backend
│   ├── package.json
│   └── vite.config.ts
├── reports/latest/             # Reportes HTML generados por CLI
├── src/
│   ├── application/
│   │   └── use_cases/          # AuditBacklogUseCase
│   ├── bootstrap/
│   │   └── dependency_injection.py # Composition Root
│   ├── domain/
│   │   ├── entities/           # AuditReport, Finding, Issue, Rule
│   │   ├── rules/              # Reglas automáticas de calidad
│   │   └── services/           # RuleEngine, ScoreService
│   ├── infrastructure/
│   │   ├── configuration/      # JiraConfig
│   │   └── jira/               # JiraClient, JiraMapper
│   └── presentation/
│       ├── api/                # FastAPI REST API (app, routes, schemas, mappers)
│       ├── cli/                # CLI parser y renderizador de consola
│       └── html/               # HtmlReportGenerator
├── tests/
│   └── unit/                   # Tests unitarios de API, RuleEngine, ScoreService
├── .dockerignore
├── .env.example
├── docker-compose.yml
├── Dockerfile                  # Python 3.11-slim non-root container
├── main.py                     # Entry point CLI
├── pyproject.toml
└── requirements.txt
```

---

# Variables de Entorno

Crea un archivo `.env` en la raíz de `apps/backlog-review-agent/` con tus credenciales de Jira a partir de la plantilla:

```bash
cp .env.example .env
```

Contenido del archivo `.env`:

```env
# Conexión a Jira Cloud (Backend)
JIRA_URL=https://tu-organizacion.atlassian.net
JIRA_EMAIL=tu-email@empresa.com
JIRA_API_TOKEN=tu_api_token_de_jira

# Configuración CORS para la API Web (Opcional, valores por defecto listos para desarrollo)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000
```

> [!IMPORTANT]
> Las credenciales de Jira permanecen en el backend y **nunca** se envían al frontend, no se incluyen en las imágenes Docker ni se exponen en los logs.

---

# Docker

El Backlog Review Agent está completamente dockerizado con una arquitectura multicontenedor basada en **Docker Compose**, **FastAPI** y **Nginx**.

```text
                     Navegador / Host
                            │
             ┌──────────────┴──────────────┐
             │  http://localhost:5173      │  http://localhost:8000
             ▼                             ▼
  ┌──────────────────────────────────────────────────┐
  │               Frontend Container                 │
  │                 (nginx:alpine)                   │
  │  Puerto interno 80 (expuesto como 5173 en host)  │
  │                                                  │
  │  /           →  React Static SPA                 │
  │  /api/       →  Proxy a http://backend:8000/api/ │
  │  /health     →  Proxy a http://backend:8000/health
  └────────────────────────┬─────────────────────────┘
                           │ Red Docker: backlog-network
                           ▼
  ┌──────────────────────────────────────────────────┐
  │               Backend Container                  │
  │          (python:3.11-slim appuser)              │
  │  Puerto interno 8000 (expuesto como 8000 en host)│
  │                                                  │
  │  FastAPI / Uvicorn (:8000)                       │
  │  - Health Check: GET /health                    │
  │  - Volumen persistente: ./reports -> /app/reports│
  └────────────────────────┬─────────────────────────┘
                           │
                           ▼
                  Jira Cloud REST API v3
```

### Requisitos

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)

### Configuración previa

1. Clona el repositorio y navega al directorio del agente:
   ```bash
   cd apps/backlog-review-agent
   ```
2. Crea tu archivo de variables de entorno a partir de la plantilla:
   ```bash
   cp .env.example .env
   ```
3. Edita `.env` con tus credenciales reales de Jira Cloud.

### Iniciar con Docker Compose

Para construir las imágenes e iniciar todos los servicios en segundo plano:

```bash
docker compose up -d --build
```

### URLs de Acceso

| Servicio | URL | Descripción |
| :--- | :--- | :--- |
| **Frontend Dashboard** | `http://localhost:5173` | Interfaz Web React para auditar backlogs |
| **Backend API** | `http://localhost:8000` | API REST FastAPI |
| **Swagger Docs** | `http://localhost:8000/docs` | Documentación interactiva OpenAPI |
| **Backend Health** | `http://localhost:8000/health` | Comprobación de estado del servicio |
| **Frontend Health Proxy**| `http://localhost:5173/health` | Healthcheck redirigido vía Nginx |

### Consultar Logs

```bash
# Ver todos los logs en tiempo real
docker compose logs -f

# Ver logs del backend únicamente
docker compose logs -f backend

# Ver logs del frontend únicamente
docker compose logs -f frontend
```

### Detener los Contenedores

```bash
docker compose down
```

### Reconstrucción limpia

```bash
docker compose build --no-cache
```

### Persistencia de Reportes

El contenedor `backend` tiene montado el volumen host `./reports:/app/reports`. Cualquier reporte HTML generado (`reports/latest/{PROJECT}_AUDIT.html`) persiste en tu máquina anfitriona y sobrevive al reinicio o eliminación de los contenedores.

---

# Cómo Iniciar en Desarrollo Local (Sin Docker)

### 1. Iniciar el Backend Web API (FastAPI)

Desde el directorio `apps/backlog-review-agent/`:

```bash
uvicorn src.presentation.api.app:app --port 8000 --reload
```

### 2. Iniciar el Frontend Web Dashboard (React)

Desde el directorio `apps/backlog-review-agent/frontend/`:

```bash
npm install
npm run dev
```

### 3. Ejecutar el flujo CLI tradicional

```bash
python main.py --project GESTADOC --max-results 100
```

---

# Endpoint Principal de la API

### `POST /api/reviews`

Ejecuta el caso de uso `AuditBacklogUseCase` y retorna el reporte formateado en DTOs de presentación.

#### Request Body

```json
{
  "project_key": "GESTADOC",
  "max_results": 100
}
```

#### Response Body (HTTP 200 OK)

```json
{
  "project": {
    "key": "GESTADOC",
    "name": null
  },
  "quality_score": 83.73,
  "statistics": {
    "total_issues": 100,
    "total_findings": 762,
    "passed": 638,
    "warnings": 0,
    "failed": 124,
    "blocked": 0
  },
  "findings": [
    {
      "rule_id": "BR-008",
      "rule_name": "Missing Acceptance Criteria",
      "issue_key": "GESTADOC-123",
      "issue_type": "Story",
      "status": "FAIL",
      "severity": "HIGH",
      "message": "No cumple la regla: Missing Acceptance Criteria.",
      "recommendation": "Definir criterios de aceptación en formato Given-When-Then o lista verificable."
    }
  ]
}
```

---

# Ejecución de Tests

Para ejecutar la suite completa de pruebas unitarias:

```bash
pytest
```

---

# Licencia

Uso interno AI-QA-Agents. Todos los derechos reservados.