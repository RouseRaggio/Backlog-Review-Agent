"""
Unit Tests for Test Case Generator API (/api/test-cases/generate & /health).
"""

import pytest
from fastapi.testclient import TestClient

from src.presentation.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "test-case-generator-agent"}


def test_api_generate_success(client):
    payload = {
        "project_key": "GES",
        "issue_key": "GES-123",
        "user_story": "Como administrador quiero gestionar usuarios para controlar accesos.",
        "acceptance_criteria": [
            {"id": "AC-001", "description": "El administrador puede crear un usuario proporcionando nombre, correo y rol."},
            {"id": "AC-002", "description": "El correo electrónico debe ser único."}
        ],
        "options": {
            "include_positive": True,
            "include_negative": True,
            "include_validation": True,
            "include_boundary": True,
            "detail_level": "standard",
            "min_priority": "LOW"
        }
    }

    response = client.post("/api/test-cases/generate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["project"]["key"] == "GES"
    assert data["project"]["issue_key"] == "GES-123"
    assert data["summary"]["total_cases"] >= 2
    assert data["summary"]["positive_count"] >= 1
    assert data["summary"]["negative_count"] >= 1
    assert len(data["test_cases"]) == data["summary"]["total_cases"]
    assert "AC-001" in data["traceability"]


def test_api_generate_empty_project_validation_error(client):
    payload = {
        "project_key": "   ",
        "issue_key": "GES-123",
        "user_story": "Historia",
        "acceptance_criteria": []
    }
    response = client.post("/api/test-cases/generate", json=payload)
    assert response.status_code == 422


from unittest.mock import patch

def test_api_generate_empty_story_without_jira_returns_400(client):
    with patch("src.infrastructure.jira.jira_config.JiraConfig.is_configured", return_value=False):
        payload = {
            "project_key": "GES",
            "issue_key": "GES-123",
            "user_story": "   ",
            "acceptance_criteria": []
        }
        response = client.post("/api/test-cases/generate", json=payload)
        assert response.status_code == 400




def test_api_generate_without_criteria(client):
    payload = {
        "project_key": "CAP",
        "issue_key": "CAP-456",
        "user_story": "Como usuario quiero visualizar mis reportes de auditoría.",
        "acceptance_criteria": []
    }
    response = client.post("/api/test-cases/generate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["summary"]["total_cases"] >= 1
    assert any("criterios de aceptación no fueron proporcionados" in w for w in data["warnings"])
    assert data["summary"]["overall_confidence"] == "LOW"
