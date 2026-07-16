"""
Rule Engine

Responsabilidad:
Ejecutar todas las reglas automáticas sobre un Issue
y generar los hallazgos correspondientes.
"""

from __future__ import annotations

from src.domain.entities.finding import Finding
from src.domain.entities.issue import Issue
from src.domain.entities.rule import Rule
from src.domain.rules.automatic_rules import AUTOMATIC_RULES


class RuleEngine:
    """
    Ejecuta las reglas automáticas de auditoría.
    """

    def __init__(self, rules: list[Rule] | None = None):
        self._rules = rules or AUTOMATIC_RULES

    def evaluate(self, issue: Issue) -> list[Finding]:
        """
        Ejecuta todas las reglas aplicables sobre un Issue.

        Parameters
        ----------
        issue : Issue

        Returns
        -------
        list[Finding]
        """

        findings: list[Finding] = []

        for rule in self._rules:

            # -----------------------------
            # ¿La regla aplica al Issue?
            # -----------------------------

            if not rule.applies_to_issue(issue.issue_type):
                continue

            # -----------------------------
            # Obtener el valor del campo
            # -----------------------------

            value = getattr(issue, rule.field, None)

            # -----------------------------
            # Evaluar regla
            # -----------------------------

            if self._is_valid(value):

                findings.append(
                    Finding(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        issue_key=issue.key,
                        issue_type=issue.issue_type,
                        status="PASS",
                        severity=None,
                        message="Regla cumplida.",
                        recommendation=None,
                    )
                )

            else:

                findings.append(
                    Finding(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        issue_key=issue.key,
                        issue_type=issue.issue_type,
                        status="FAIL",
                        severity=rule.severity,
                        message=f"No cumple la regla: {rule.name}.",
                        recommendation=rule.recommendation,
                    )
                )

        return findings

    @staticmethod
    def _is_valid(value) -> bool:
        """
        Determina si un valor cumple la regla.

        Se considera inválido:

        - None
        - ""
        - []
        """

        if value is None:
            return False

        if isinstance(value, str):
            return bool(value.strip())

        if isinstance(value, list):
            return len(value) > 0

        return True