"""
Composition Root: Dependency Injection

Ensambla todas las dependencias de la aplicación
siguiendo Clean Architecture.
"""

from __future__ import annotations

from src.application.use_cases.audit_backlog import AuditBacklogUseCase
from src.domain.services.rule_engine import RuleEngine
from src.domain.services.score_service import ScoreService
from src.infrastructure.jira.jira_client import JiraClient


def build_application() -> AuditBacklogUseCase:
    """
    Construye las dependencias de la aplicación.
    """

    jira_client = JiraClient()

    rule_engine = RuleEngine()

    score_service = ScoreService()

    return AuditBacklogUseCase(
        jira_client=jira_client,
        rule_engine=rule_engine,
        score_service=score_service,
    )
