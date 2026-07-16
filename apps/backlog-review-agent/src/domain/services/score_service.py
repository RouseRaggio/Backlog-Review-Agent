"""
Domain Service: Score Service

Calcula el Backlog Quality Score de una auditoría.
"""

from __future__ import annotations

from src.domain.entities.audit_report import AuditReport


class ScoreService:
    """
    Servicio encargado de calcular el Backlog Quality Score.
    """

    def calculate(self, report: AuditReport) -> float:
        """
        Calcula el porcentaje de reglas aprobadas.

        Parameters
        ----------
        report : AuditReport

        Returns
        -------
        float
        """

        total = report.total_findings

        if total == 0:
            return 100.0

        passed = report.passed

        score = (passed / total) * 100

        return round(score, 2)