"""
Infrastructure: JiraGatewayAdapter

Implementa el puerto JiraGateway del dominio consumiendo JiraClient y CriteriaExtractor.
"""

from __future__ import annotations

from typing import Any, Optional
from src.domain.entities import AcceptanceCriterion, UserStory
from src.domain.services.jira_gateway import JiraGateway
from src.infrastructure.jira.criteria_extractor import CriteriaExtractor
from src.infrastructure.jira.jira_client import JiraClient
from src.infrastructure.jira.jira_config import JiraConfig


class JiraGatewayAdapter(JiraGateway):
    """
    Adaptador de infraestructura para Jira.
    """

    def __init__(
        self,
        client: Optional[JiraClient] = None,
        config: Optional[JiraConfig] = None,
    ):
        self._config = config or JiraConfig.from_env()
        self._client = client or JiraClient(config=self._config)

    def get_user_story(
        self,
        project_key: str,
        issue_key: str,
    ) -> tuple[UserStory, list[AcceptanceCriterion], list[str], dict[str, Any]]:
        """
        Consulta Jira, construye el objeto UserStory y extrae sus Criterios de Aceptación y Pruebas QA.
        """
        raw_issue = self._client.get_issue(project_key=project_key, issue_key=issue_key)
        fields = raw_issue.get("fields", {})

        summary = fields.get("summary") or ""
        description_raw = fields.get("description")
        description_text = JiraClient.extract_text(description_raw) or ""

        # Extraer criterios de aceptación, pruebas QA y DoD
        criteria, qa_tests, dod_items = CriteriaExtractor.extract_from_fields(
            fields=fields,
            custom_ac_field_id=self._config.acceptance_criteria_field,
        )

        # Construir UserStory
        full_story_text = description_text if description_text else summary
        story = UserStory(
            project_key=project_key,
            issue_key=issue_key,
            title=summary,
            raw_text=full_story_text,
        )

        metadata = {
            "id": raw_issue.get("id"),
            "key": raw_issue.get("key"),
            "issue_type": fields.get("issuetype", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "status": fields.get("status", {}).get("name"),
            "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
            "labels": fields.get("labels", []),
            "components": [c.get("name") for c in fields.get("components", []) if c.get("name")],
            "definition_of_done": dod_items,
        }

        return story, criteria, qa_tests, metadata
