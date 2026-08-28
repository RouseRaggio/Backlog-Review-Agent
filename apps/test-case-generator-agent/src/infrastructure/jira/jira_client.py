"""
Infrastructure: Jira REST Client
"""

from __future__ import annotations

import logging
from typing import Any, Optional
import requests

from src.domain.services.jira_gateway import (
    JiraConfigError,
    JiraConnectionError,
    JiraError,
    JiraPermissionError,
    JiraTimeoutError,
    UserStoryNotFoundError,
)
from src.infrastructure.jira.jira_config import JiraConfig

logger = logging.getLogger(__name__)


class JiraClient:
    """
    Cliente HTTP desacoplado para consultar Jira Cloud REST API.
    """

    def __init__(self, config: Optional[JiraConfig] = None):
        self._config = config or JiraConfig.from_env()

    def get_issue(self, project_key: str, issue_key: str) -> dict[str, Any]:
        """
        Obtiene los datos crudos de una Issue desde Jira.
        """
        if not self._config.is_configured():
            raise JiraConfigError("La integración con Jira no está configurada correctamente.")

        url = f"{self._config.base_url}/rest/api/3/issue/{issue_key}"
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(
                url,
                headers=headers,
                auth=(self._config.email, self._config.token),
                timeout=15,
            )

            if response.status_code == 404:
                raise UserStoryNotFoundError(f"Historia de Usuario '{issue_key}' no encontrada en Jira.")

            if response.status_code in (401, 403):
                raise JiraPermissionError("No tienes permisos para consultar esta Issue en Jira.")

            if response.status_code >= 500:
                raise JiraConnectionError("No fue posible comunicarse con Jira (error del servidor).")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout al consultar issue {issue_key} en Jira.")
            raise JiraTimeoutError("Jira no respondió dentro del tiempo esperado.")

        except requests.exceptions.ConnectionError:
            logger.warning(f"Error de conexión con Jira para issue {issue_key}.")
            raise JiraConnectionError("No fue posible comunicarse con Jira.")

        except JiraError:
            raise

        except Exception as e:
            logger.exception(f"Error inesperado al consultar Jira: {e}")
            raise JiraConnectionError("Ocurrió un error inesperado al conectar con Jira.")

    @staticmethod
    def extract_text(value: Any) -> Optional[str]:
        """
        Convierte el formato Atlassian Document Format (ADF) o valores mixtos en texto plano estructurado.
        """
        from src.infrastructure.jira.adf_parser import ADFParser
        return ADFParser.to_text(value)

