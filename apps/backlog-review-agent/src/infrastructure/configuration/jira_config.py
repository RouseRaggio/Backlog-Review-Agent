"""
Jira Configuration

Carga y valida la configuración de conexión a Jira
desde variables de entorno.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class JiraConfig:
    base_url: str
    email: str
    token: str

    @classmethod
    def from_env(cls) -> JiraConfig:
        base_url = os.getenv("JIRA_URL")
        email = os.getenv("JIRA_EMAIL")
        token = os.getenv("JIRA_API_TOKEN")

        if not base_url:
            raise ValueError("JIRA_URL no configurada")

        if not email:
            raise ValueError("JIRA_EMAIL no configurado")

        if not token:
            raise ValueError("JIRA_API_TOKEN no configurado")

        return cls(
            base_url=base_url,
            email=email,
            token=token,
        )
