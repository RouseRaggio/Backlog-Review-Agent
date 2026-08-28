"""
Infrastructure: Jira Configuration
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class JiraConfig:
    """
    Configuración de conexión a Jira Cloud.
    """

    base_url: str
    email: str
    token: str
    acceptance_criteria_field: Optional[str] = None

    @classmethod
    def from_env(cls) -> JiraConfig:
        """
        Carga la configuración desde las variables de entorno.
        """
        base_url = (os.getenv("JIRA_URL") or "").rstrip("/")
        email = os.getenv("JIRA_EMAIL") or ""
        token = os.getenv("JIRA_API_TOKEN") or ""
        ac_field = os.getenv("JIRA_ACCEPTANCE_CRITERIA_FIELD") or None

        return cls(
            base_url=base_url,
            email=email,
            token=token,
            acceptance_criteria_field=ac_field,
        )

    def is_configured(self) -> bool:
        """
        Verifica si los parámetros obligatorios están presentes.
        """
        return bool(self.base_url and self.email and self.token)
