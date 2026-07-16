"""
Jira Mapper

Responsabilidad:
- Convertir el JSON de Jira en objetos del dominio (Issue).

No contiene reglas de negocio.
No conoce el RuleEngine.
No conoce la IA.
"""

from __future__ import annotations

from src.domain.models.issue import Issue


class JiraMapper:

    @staticmethod
    def to_issue(jira_issue: dict) -> Issue:

        fields = jira_issue.get("fields", {})

        # -------------------------------------------------
        # Descripción
        # -------------------------------------------------

        description = JiraMapper._extract_text(
            fields.get("description")
        )

        # -------------------------------------------------
        # Responsable
        # -------------------------------------------------

        assignee = None

        if fields.get("assignee"):

            assignee = fields["assignee"].get(
                "displayName"
            )

        # -------------------------------------------------
        # Epic (Parent)
        # -------------------------------------------------

        epic = None

        parent = fields.get("parent")

        if parent:

            parent_fields = parent.get("fields", {})

            issue_type = (
                parent_fields
                .get("issuetype", {})
                .get("name")
            )

            if issue_type == "Epic":

                epic = parent.get("key")

        # -------------------------------------------------
        # Story Points
        # (Se ajustará cuando identifiquemos el customfield)
        # -------------------------------------------------

        story_points = None

        # -------------------------------------------------
        # Sprint
        # (Se ajustará cuando identifiquemos el customfield)
        # -------------------------------------------------

        sprint = None

        # -------------------------------------------------
        # Acceptance Criteria
        # (Se ajustará cuando identifiquemos el customfield)
        # -------------------------------------------------

        acceptance_criteria = None

        # -------------------------------------------------
        # Crear objeto del dominio
        # -------------------------------------------------

        return Issue(

            id=jira_issue.get("id"),

            key=jira_issue.get("key"),

            summary=fields.get("summary"),

            description=description,

            issue_type=(
                fields
                .get("issuetype", {})
                .get("name")
            ),

            priority=(
                fields
                .get("priority", {})
                .get("name")
            ),

            status=(
                fields
                .get("status", {})
                .get("name")
            ),

            assignee=assignee,

            epic=epic,

            sprint=sprint,

            story_points=story_points,

            acceptance_criteria=acceptance_criteria,
        )

    @staticmethod
    def _extract_text(value) -> str | None:
        """
        Convierte el formato Atlassian Document Format
        (ADF) en texto plano.
        """

        if value is None:
            return None

        if not isinstance(value, dict):
            return str(value)

        result = []

        def walk(node):

            if isinstance(node, dict):

                if node.get("type") == "text":

                    result.append(node.get("text", ""))

                for child in node.get("content", []):

                    walk(child)

            elif isinstance(node, list):

                for item in node:

                    walk(item)

        walk(value)

        text = "\n".join(result).strip()

        return text if text else None