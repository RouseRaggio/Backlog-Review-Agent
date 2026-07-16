"""
Jira REST Client

Responsabilidad:
- Conectarse a Jira Cloud.
- Ejecutar consultas JQL.
- Obtener Issues.

No contiene reglas de negocio.
No conoce nada sobre IA.
"""

import os

import requests
from dotenv import load_dotenv

from src.domain.models.issue import Issue
from src.infrastructure.jira.jira_mapper import JiraMapper

load_dotenv()


class JiraClient:

    def __init__(self):

        self.base_url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")

        if not self.base_url:
            raise ValueError("JIRA_URL no configurada")

        if not self.email:
            raise ValueError("JIRA_EMAIL no configurado")

        if not self.token:
            raise ValueError("JIRA_API_TOKEN no configurado")

        self.headers = {
            "Accept": "application/json"
        }

    def get_issues(
        self,
        project_key: str,
        max_results: int = 50,
    ) -> list[Issue]:
        """
        Obtiene los Issues de un proyecto.
        """

        url = f"{self.base_url}/rest/api/3/search/jql"

        params = {
            "jql": f"project = {project_key}",
            "maxResults": max_results,
            "fields": (
                "summary,"
                "description,"
                "issuetype,"
                "priority,"
                "status,"
                "assignee,"
                "parent"
            ),
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            auth=(self.email, self.token),
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        issues: list[Issue] = []

        for jira_issue in data.get("issues", []):

            issues.append(
                JiraMapper.to_issue(jira_issue)
            )

        return issues