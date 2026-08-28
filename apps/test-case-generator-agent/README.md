# Test Case Generator Agent

## Descripción

**Test Case Generator Agent** es el segundo agente del ecosistema **AI-QA-Agents**. Su propósito es recibir Historias de Usuario y Criterios de Aceptación para generar automáticamente casos de prueba estructurados, trazables y clasificados (positivos, negativos, de validación y límites).

### Principio Fundamental: NO INVENTAR (Strict Grounding)

> *"Es preferible generar menos casos de prueba correctamente trazables que generar muchos casos basados en supuestos."*

El agente diferencia estrictamente entre:
- **Información Conocida**: Cláusulas expresadas directamente en la Historia o los Criterios.
- **Información Desconocida**: Omisiones de reglas, formatos, longitudes o expresiones regulares.

El agente **no inventa** restricciones ni validaciones que no figuren en la entrada. Si la información para casos límite o criterios es insuficiente, degrada el nivel de confianza (`confidence: LOW`) y emite advertencias explícitas.

---

# Arquitectura

El agente sigue **Clean Architecture** y **SOLID**:

```text
                        ┌──────────────────────────────┐
                        │      PRESENTATION LAYER      │
                        │                              │
                        │  CLI:      main.py           │
                        │  REST API: FastAPI (routes)  │
                        │  Web UI:   React TypeScript  │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │      APPLICATION LAYER       │
                        │                              │
                        │   GenerateTestCasesUseCase   │
                        └──────────────┬───────────────┘
                                       │
                        ┌──────────────┴───────────────┐
                        ▼                              ▼
          ┌───────────────────────────┐  ┌───────────────────────────┐
          │       DOMAIN LAYER        │  │   INFRASTRUCTURE LAYER    │
          │                           │  │                           │
          │ Entities: UserStory,      │  │ RuleBasedTestCaseGenerator│
          │           TestCase,       │  │ LLMTestCaseGenerator(Stub)│
          │           AcceptanceCrit  │  │                           │
          │ Services: SufficiencyVal, │  │                           │
          │           TraceabilitySvc │  │                           │
          └───────────────────────────┘  └───────────────────────────┘
```

### Estructura de Carpetas

```text
apps/test-case-generator-agent/
├── config/                     # Configuraciones del agente
├── docs/                       # Documentación técnica
├── frontend/                   # Dashboard React 18 + TS + Vite + Tailwind
│   ├── src/
│   │   ├── components/         # Sidebar, StoryInputForm, CriteriaListEditor, TestCasesTable, etc.
│   │   ├── services/           # Cliente API HTTP
│   │   ├── types/              # DTOs TypeScript
│   │   ├── App.tsx             # Dashboard principal Dark UI
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── nginx.conf              # Reverse proxy /api/ -> backend:8000
│   └── package.json
├── src/
│   ├── application/
│   │   └── use_cases/          # GenerateTestCasesUseCase
│   ├── bootstrap/
│   │   └── dependency_injection.py # Composition Root
│   ├── domain/
│   │   ├── entities/           # UserStory, AcceptanceCriterion, TestCase, GenerationResult
│   │   ├── enums/              # TestCaseType, Category, Priority, Status, Confidence
│   │   └── services/           # TestCaseGenerator (Port), SufficiencyValidator, TraceabilityService
│   ├── infrastructure/
│   │   ├── ai/                 # LLMTestCaseGenerator (Stub preparado)
│   │   └── generators/         # RuleBasedTestCaseGenerator (MVP determinista)
│   └── presentation/
│       ├── api/                # FastAPI REST API (app, routes, schemas, mappers)
│       └── cli/                # CLI Runner
├── tests/
│   └── unit/                   # Tests unitarios de dominio, motor de reglas, no-invención y API
├── .dockerignore
├── .env.example
├── docker-compose.yml          # Backend: 8001:8000, Frontend: 5174:80
├── Dockerfile                  # Python 3.11-slim
├── main.py                     # Entry point CLI
├── pyproject.toml
└── requirements.txt
```

---

# Jira Integration & Workflow

A partir de la versión actual, **Jira Cloud es la fuente principal de información**. El usuario solo necesita proporcionar el Proyecto (ej. `GES`) y el Issue Key (ej. `GES-40`), y el agente se encarga de consultar Jira, extraer la Historia de Usuario y sus Criterios de Aceptación, evaluar la suficiencia de información y sintetizar los casos de prueba.

### Flujo de Trabajo

```text
Usuario (Proyecto: GES, Issue: GES-40)
  ↓
Test Case Generator Agent
  ↓
Jira Cloud REST API (/rest/api/3/issue/{issue_key})
  ↓
Obtener Historia de Usuario + Criterios (Custom Field o Descripción)
  ↓
POST /api/test-cases/analyze (Diagnóstico previo, suficiencia y confianza)
  ↓
POST /api/test-cases/generate (Sintetizar casos positivos, negativos, validación y límites)
  ↓
Matriz de Trazabilidad y Casos Estructurados
```

### Modos de Operación

1. **Modo Jira (Principal):** El agente consulta Jira automáticamente. Si los criterios no están explícitos, emite advertencias y marca `status: REVIEW_REQUIRED` sin inventar requerimientos.
2. **Modo Manual (Fallback):** Permite ingresar o editar manualmente la Historia de Usuario y los Criterios de Aceptación para casos donde Jira no esté disponible o para pruebas locales ad-hoc.

---

# Variables de Entorno

Configurar en el archivo `.env`:

```bash
# Jira Cloud Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-api-token

# Opcional: ID del custom field para Criterios de Aceptación (ej. customfield_10038)
# Si está vacío, los criterios se extraen de la descripción de la Issue
JIRA_ACCEPTANCE_CRITERIA_FIELD=
```

---

# API REST

### 1. `POST /api/test-cases/analyze`

Consulta Jira y analiza la Historia de Usuario diagnosticando la suficiencia de información antes de generar los casos de prueba.

#### Request Body
```json
{
  "project_key": "GES",
  "issue_key": "GES-40"
}
```

#### Response Body (HTTP 200 OK)
```json
{
  "project": {
    "key": "GES",
    "issue_key": "GES-40"
  },
  "user_story": {
    "title": "Gestión de usuarios del sistema",
    "raw_text": "Como administrador del sistema quiero gestionar usuarios para controlar accesos."
  },
  "acceptance_criteria": [
    {
      "id": "AC-001",
      "description": "El administrador puede crear un usuario con nombre y rol."
    },
    {
      "id": "AC-002",
      "description": "El sistema valida que el correo sea único."
    }
  ],
  "source": "jira",
  "sufficient_information": true,
  "confidence": "HIGH",
  "warnings": []
}
```

---

### 2. `POST /api/test-cases/generate`

Genera casos de prueba estructurados y trazables a partir de Jira o del payload manual.

#### Request Body (Modo Jira Directo)

```json
{
  "project_key": "GES",
  "issue_key": "GES-40",
  "options": {
    "include_positive": true,
    "include_negative": true,
    "include_validation": true,
    "include_boundary": true,
    "detail_level": "standard",
    "min_priority": "LOW"
  }
}
```


#### Response Body (HTTP 200 OK)

```json
{
  "project": {
    "key": "GES",
    "issue_key": "GES-123"
  },
  "summary": {
    "total_cases": 2,
    "positive_count": 1,
    "negative_count": 1,
    "validation_count": 0,
    "boundary_count": 0,
    "traceability_rate": 100.0,
    "overall_confidence": "HIGH"
  },
  "warnings": [
    "No se generaron casos límite porque la Historia de Usuario y los criterios de aceptación no especifican valores límite o umbrales."
  ],
  "test_cases": [
    {
      "id": "TC-GES-123-001",
      "title": "Crear un usuario proporcionando nombre, correo electrónico y rol",
      "description": "Verificar el comportamiento positivo del criterio AC-001.",
      "type": "POSITIVE",
      "category": "FUNCTIONAL",
      "priority": "HIGH",
      "preconditions": [
        "El usuario ha iniciado sesión como Administrador."
      ],
      "required_data": {
        "nombre": "Valor válido para nombre",
        "correo electrónico": "Valor válido para correo electrónico",
        "rol": "Valor válido para rol"
      },
      "steps": [
        "1. Acceder a la interfaz correspondiente al criterio AC-001.",
        "2. Ingresar la información requerida: nombre, correo electrónico, rol.",
        "3. Ejecutar la acción."
      ],
      "expected_result": "La acción se completa exitosamente conforme al criterio.",
      "requirement_reference": "GES-123",
      "acceptance_criteria_reference": "AC-001",
      "confidence": "HIGH",
      "status": "READY"
    },
    {
      "id": "TC-GES-123-002",
      "title": "Validar rechazo de correo electrónico duplicado",
      "description": "Verificar que el sistema rechaza la operación si el correo electrónico ya existe en el sistema.",
      "type": "NEGATIVE",
      "category": "VALIDATION",
      "priority": "CRITICAL",
      "preconditions": [
        "El usuario ha iniciado sesión como Administrador.",
        "Existe un registro previo en el sistema con el correo electrónico de prueba."
      ],
      "required_data": {
        "correo electrónico": "valor_ya_registrado@ejemplo.com"
      },
      "steps": [
        "1. Intentar registrar una entidad utilizando un correo electrónico ya existente.",
        "2. Confirmar la operación."
      ],
      "expected_result": "El sistema rechaza la operación e informa que el correo electrónico ya se encuentra registrado.",
      "requirement_reference": "GES-123",
      "acceptance_criteria_reference": "AC-002",
      "confidence": "HIGH",
      "status": "READY"
    }
  ],
  "traceability": {
    "AC-001": ["TC-GES-123-001"],
    "AC-002": ["TC-GES-123-002"]
  }
}
```

---

# Cómo Iniciar en Desarrollo Local (Sin Docker)

### 1. Iniciar el Backend API (FastAPI)

```bash
cd apps/test-case-generator-agent
uvicorn src.presentation.api.app:app --port 8001 --reload
```
- API URL: `http://localhost:8001`
- Swagger Docs: `http://localhost:8001/docs`
- Health Check: `http://localhost:8001/health`

### 2. Iniciar el Frontend Dashboard (React)

```bash
cd apps/test-case-generator-agent/frontend
npm install
npm run dev
```
- Frontend Dashboard: `http://localhost:5174`

### 3. Ejecutar por CLI

```bash
cd apps/test-case-generator-agent
python main.py --project GES --issue GES-123 --story "Como administrador quiero gestionar usuarios" --criteria "El correo debe ser único"
```

---

# Docker

El agente cuenta con su propia configuración Docker Compose en puertos aislados para ejecutarse simultáneamente con el Backlog Review Agent.

| Agente | Backend Port | Frontend Port | Red Docker |
| :--- | :--- | :--- | :--- |
| **Backlog Review Agent** | `8000` | `5173` | `backlog-network` |
| **Test Case Generator Agent** | `8001` | `5174` | `test-case-generator-network` |

### Iniciar con Docker Compose

```bash
cd apps/test-case-generator-agent
cp .env.example .env
docker compose up -d --build
```

- **Frontend:** [http://localhost:5174](http://localhost:5174)
- **Backend API:** [http://localhost:8001](http://localhost:8001)

---

# Ejecución de Tests

Para ejecutar la suite de pruebas unitarias:

```bash
cd apps/test-case-generator-agent
pytest
```

---

# Integración Futura

- **Integración con Backlog Review Agent:** El Test Case Generator Agent está diseñado para consumir directamente las historias auditadas y aprobadas por el Backlog Review Agent.
- **Integración con LLMs:** La interfaz `TestCaseGenerator` permite conectar proveedores como OpenAI, Anthropic Claude o modelos locales (Ollama/Qwen) manteniendo intactas las entidades de dominio, el caso de uso y los contratos de API.

---

# Licencia

Uso interno AI-QA-Agents. Todos los derechos reservados.
