"""
Application Use Case: Audit Backlog

Orquesta una auditoría completa de un Backlog de Jira.

Responsabilidades
-----------------
- Obtener los Issues desde Jira.
- Ejecutar el Rule Engine.
- Construir el Audit Report.
- Calcular el Backlog Quality Score.

No contiene reglas de negocio.
No conoce la API REST de Jira.
No conoce Markdown.
No conoce IA.
"""

from __future__ import annotations

from src.domain.models.audit_report import AuditReport
from src.domain.services.rule_engine import RuleEngine
from src.domain.services.score_service import ScoreService
from src.infrastructure.jira.jira_client import JiraClient


class AuditBacklogUseCase:

    def __init__(
        self,
        jira_client: JiraClient,
        rule_engine: RuleEngine,
        score_service: ScoreService,
    ):

        self._jira = jira_client
        self._rule_engine = rule_engine
        self._score_service = score_service

    def execute(
        self,
        project_key: str,
        max_results: int = 100,
    ) -> AuditReport:
        """
        Ejecuta una auditoría completa.

        Parameters
        ----------
        project_key
            Clave del proyecto Jira.

        max_results
            Número máximo de Issues.

        Returns
        -------
        AuditReport
        """

        # ------------------------------------------
        # Obtener Issues
        # ------------------------------------------

        issues = self._jira.get_issues(
            project_key=project_key,
            max_results=max_results,
        )

        # ------------------------------------------
        # Crear Reporte
        # ------------------------------------------

        report = AuditReport(
            project_key=project_key,
        )

        # ------------------------------------------
        # Auditar cada Issue
        # ------------------------------------------

        for issue in issues:

            findings = self._rule_engine.evaluate(issue)

            report.extend(findings)

        # ------------------------------------------
        # Calcular Score
        # ------------------------------------------

        report.quality_score = self._score_service.calculate(
            report
        )

        return report