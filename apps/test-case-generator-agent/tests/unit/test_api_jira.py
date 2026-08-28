"""
Unit and Integration Tests for Jira REST API Endpoints.
"""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.presentation.api.app import app
from src.domain.services.jira_gateway import (

    JiraConnectionError,
    JiraPermissionError,
    UserStoryNotFoundError,
)

client = TestClient(app)


@patch("src.infrastructure.jira.jira_gateway_adapter.JiraGatewayAdapter.get_user_story")
def test_api_analyze_user_story_success(mock_get_story):
    from src.domain.entities import AcceptanceCriterion, UserStory

    story = UserStory(
        project_key="GES",
        issue_key="GES-40",
        title="Gestión de usuarios",
        raw_text="Como admin quiero gestionar usuarios para seguridad.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-001", description="El admin puede crear un nuevo usuario."),
    ]
    qa_tests = ["Prueba de creación."]
    mock_get_story.return_value = (story, criteria, qa_tests, {"status": "In Progress"})


    response = client.post(
        "/api/test-cases/analyze",
        json={"project_key": "GES", "issue_key": "GES-40"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["project"]["key"] == "GES"
    assert data["project"]["issue_key"] == "GES-40"
    assert data["source"] == "jira"
    assert len(data["acceptance_criteria"]) == 1


@patch("src.infrastructure.jira.jira_gateway_adapter.JiraGatewayAdapter.get_user_story")
def test_api_analyze_user_story_404_not_found(mock_get_story):
    mock_get_story.side_effect = UserStoryNotFoundError("Historia GES-99 no encontrada.")

    response = client.post(
        "/api/test-cases/analyze",
        json={"project_key": "GES", "issue_key": "GES-99"},
    )

    assert response.status_code == 404
    data = response.json()
    assert "no encontrada" in data["detail"]


@patch("src.infrastructure.jira.jira_gateway_adapter.JiraGatewayAdapter.get_user_story")
def test_api_analyze_user_story_403_permission(mock_get_story):
    mock_get_story.side_effect = JiraPermissionError("Permisos insuficientes.")

    response = client.post(
        "/api/test-cases/analyze",
        json={"project_key": "GES", "issue_key": "GES-40"},
    )

    assert response.status_code == 403


@patch("src.infrastructure.jira.jira_gateway_adapter.JiraGatewayAdapter.get_user_story")
def test_api_generate_with_jira_automatic(mock_get_story):
    from src.domain.entities import AcceptanceCriterion, UserStory

    story = UserStory(
        project_key="GES",
        issue_key="GES-40",
        title="Gestión de usuarios",
        raw_text="Como admin quiero gestionar usuarios para seguridad.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-001", description="El admin puede crear un nuevo usuario con rol."),
    ]
    qa_tests = ["Prueba de creación."]
    mock_get_story.return_value = (story, criteria, qa_tests, {})


    response = client.post(
        "/api/test-cases/generate",
        json={
            "project_key": "GES",
            "issue_key": "GES-40",
            "options": {
                "include_positive": True,
                "include_negative": True,
                "include_validation": True,
                "include_boundary": True,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["project"]["key"] == "GES"
    assert data["summary"]["total_cases"] > 0


def test_api_generate_with_manual_fallback():
    response = client.post(
        "/api/test-cases/generate",
        json={
            "project_key": "MANUAL",
            "issue_key": "MAN-1",
            "user_story": "Como usuario quiero autenticarme para acceder.",
            "acceptance_criteria": [
                {"id": "AC-001", "description": "Ingresar credenciales correctas."}
            ],
            "options": {
                "include_positive": True,
                "include_negative": True,
                "include_validation": True,
                "include_boundary": True,
            },
        },
    )


    assert response.status_code == 200
    data = response.json()
    assert data["project"]["key"] == "MANUAL"
    assert data["summary"]["total_cases"] > 0
