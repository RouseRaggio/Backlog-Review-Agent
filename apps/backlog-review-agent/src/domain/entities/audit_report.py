"""
Domain Model: Audit Report

Representa el resultado completo de una auditoría
sobre un Backlog de Jira.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.domain.entities.finding import Finding


@dataclass(slots=True)
class AuditReport:
    """
    Resultado de una auditoría de Backlog.
    """

    # ---------------------------------------------------------
    # Información del proyecto
    # ---------------------------------------------------------

    project_key: str

    project_name: str | None = None

    # ---------------------------------------------------------
    # Resultados
    # ---------------------------------------------------------

    findings: list[Finding] = field(default_factory=list)

    quality_score: float = 0.0

    # ---------------------------------------------------------
    # Operaciones
    # ---------------------------------------------------------

    def add_finding(self, finding: Finding) -> None:
        """Agrega un hallazgo al reporte."""

        self.findings.append(finding)

    def extend(self, findings: list[Finding]) -> None:
        """Agrega varios hallazgos."""

        self.findings.extend(findings)

    # ---------------------------------------------------------
    # Estadísticas
    # ---------------------------------------------------------

    @property
    def total_findings(self) -> int:
        return len(self.findings)

    @property
    def passed(self) -> int:
        return sum(
            finding.passed
            for finding in self.findings
        )

    @property
    def warnings(self) -> int:
        return sum(
            finding.warning
            for finding in self.findings
        )

    @property
    def failed(self) -> int:
        return sum(
            finding.failed
            for finding in self.findings
        )

    @property
    def blocked(self) -> int:
        return sum(
            finding.blocked
            for finding in self.findings
        )

    @property
    def success_rate(self) -> float:

        if self.total_findings == 0:
            return 100.0

        return round(
            (self.passed / self.total_findings) * 100,
            2,
        )

    def summary(self) -> dict:
        """
        Retorna un resumen del reporte.
        """

        return {
            "project": self.project_key,
            "quality_score": self.quality_score,
            "total_findings": self.total_findings,
            "passed": self.passed,
            "warnings": self.warnings,
            "failed": self.failed,
            "blocked": self.blocked,
        }