"""
Unit Tests for JiraClient and JiraConfig.
"""

from unittest.mock import MagicMock, patch
import pytest
import requests

from src.domain.services.jira_gateway import (
    JiraConfigError,
    JiraConnectionError,
    JiraPermissionError,
    JiraTimeoutError,
    UserStoryNotFoundError,
)
from src.infrastructure.jira.jira_client import JiraClient
from src.infrastructure.jira.jira_config import JiraConfig


def test_jira_config_validation():
    config = JiraConfig(base_url="", email="", token="")
    assert not config.is_configured()

    valid_config = JiraConfig(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        token="secret-token",
    )
    assert valid_config.is_configured()


def test_jira_client_unconfigured_raises_jira_config_error():
    config = JiraConfig(base_url="", email="", token="")
    client = JiraClient(config=config)
    with pytest.raises(JiraConfigError):
        client.get_issue("GES", "GES-40")


@patch("requests.get")
def test_jira_client_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "10001",
        "key": "GES-40",
        "fields": {
            "summary": "Gestión de usuarios",
            "description": "Como administrador quiero gestionar usuarios.",
            "issuetype": {"name": "Story"},
            "priority": {"name": "High"},
            "status": {"name": "To Do"},
        },
    }
    mock_get.return_value = mock_response

    config = JiraConfig("https://example.atlassian.net", "u@e.com", "tok")
    client = JiraClient(config=config)
    result = client.get_issue("GES", "GES-40")

    assert result["key"] == "GES-40"
    assert result["fields"]["summary"] == "Gestión de usuarios"


@patch("requests.get")
def test_jira_client_404_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    config = JiraConfig("https://example.atlassian.net", "u@e.com", "tok")
    client = JiraClient(config=config)
    with pytest.raises(UserStoryNotFoundError):
        client.get_issue("GES", "NONEXIST-999")


@patch("requests.get")
def test_jira_client_401_403_permission_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    config = JiraConfig("https://example.atlassian.net", "u@e.com", "tok")
    client = JiraClient(config=config)
    with pytest.raises(JiraPermissionError):
        client.get_issue("GES", "GES-40")


@patch("requests.get")
def test_jira_client_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    config = JiraConfig("https://example.atlassian.net", "u@e.com", "tok")
    client = JiraClient(config=config)
    with pytest.raises(JiraTimeoutError):
        client.get_issue("GES", "GES-40")


def test_jira_client_extract_text_adf():
    adf_data = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Como administrador "},
                    {"type": "text", "text": "quiero gestionar usuarios."},
                ],
            }
        ],
    }
    extracted = JiraClient.extract_text(adf_data)
    assert extracted == "Como administrador quiero gestionar usuarios."

