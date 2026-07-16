"""
Jira REST Client

Responsabilidad:
- Conectarse a Jira Cloud.
- Ejecutar consultas JQL.
- Obtener Issues.

No contiene reglas de negocio.
No conoce nada sobre IA.
"""

import requests

from src.domain.entities.issue import Issue
from src.infrastructure.jira.jira_mapper import JiraMapper
from src.infrastructure.configuration.jira_config import JiraConfig


class JiraClient:

    def __init__(self, config: JiraConfig | None = None):

        self._config = config or JiraConfig.from_env()

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

        url = f"{self._config.base_url}/rest/api/3/search/jql"

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
            auth=(self._config.email, self._config.token),
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