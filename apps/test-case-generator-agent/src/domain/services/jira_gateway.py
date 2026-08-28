"""
Domain Port: JiraGateway Interface & Domain Exceptions
"""

from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities import AcceptanceCriterion, UserStory


class JiraError(Exception):
    """Excepción base para errores de integración con Jira."""
    pass


class UserStoryNotFoundError(JiraError):
    """La Historia de Usuario / Issue no existe en Jira (HTTP 404)."""
    pass


class JiraPermissionError(JiraError):
    """No se tienen permisos o credenciales inválidas para consultar la Issue (HTTP 401/403)."""
    pass


class JiraConnectionError(JiraError):
    """Fallo de conexión o error del servidor de Jira (HTTP 500/502/503)."""
    pass


class JiraTimeoutError(JiraError):
    """Tiempo de espera agotado al consultar Jira."""
    pass


class JiraConfigError(JiraError):
    """La configuración de Jira (URL, Email o Token) no está presente o es inválida."""
    pass


class JiraGateway(ABC):
    """
    Puerto para la integración desacoplada con Jira.
    """

    @abstractmethod
    def get_user_story(
        self,
        project_key: str,
        issue_key: str,
    ) -> tuple[UserStory, list[AcceptanceCriterion], list[str], dict[str, Any]]:
        """
        Obtiene una Historia de Usuario, sus Criterios de Aceptación, Pruebas QA y metadatos desde Jira.
        Retorna (UserStory, list[AcceptanceCriterion], list[qa_tests], metadata_dict).
        """
        pass
