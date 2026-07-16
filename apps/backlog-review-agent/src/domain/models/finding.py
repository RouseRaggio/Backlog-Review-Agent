"""
Domain Model: Finding

Representa el resultado de una regla de auditoría aplicada
sobre un Issue de Jira.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Finding:
    """
    Hallazgo generado durante la auditoría de un Issue.
    """

    # -------------------------
    # Regla
    # -------------------------

    rule_id: str
    rule_name: str

    # -------------------------
    # Issue auditado
    # -------------------------

    issue_key: str
    issue_type: str

    # -------------------------
    # Resultado
    # -------------------------

    status: str

    # PASS
    # WARNING
    # FAIL
    # BLOCKED
    # NOT_APPLICABLE

    severity: Optional[str] = None

    # LOW
    # MEDIUM
    # HIGH
    # CRITICAL

    # -------------------------
    # Información
    # -------------------------

    message: str = ""

    recommendation: Optional[str] = None

    # -------------------------
    # Helpers
    # -------------------------

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    @property
    def failed(self) -> bool:
        return self.status == "FAIL"

    @property
    def blocked(self) -> bool:
        return self.status == "BLOCKED"

    @property
    def warning(self) -> bool:
        return self.status == "WARNING"

    @property
    def not_applicable(self) -> bool:
        return self.status == "NOT_APPLICABLE"

    def __str__(self) -> str:
        return (
            f"[{self.status}] "
            f"{self.issue_key} | "
            f"{self.rule_id} | "
            f"{self.message}"
        )