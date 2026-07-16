"""
Domain Model: Rule

Representa una regla de auditoría del Backlog Review Agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Rule:
    """
    Define una regla de auditoría.
    """

    # -------------------------
    # Identificación
    # -------------------------

    id: str
    name: str

    # -------------------------
    # Configuración
    # -------------------------

    field: str

    applies_to: list[str]

    # True = el campo es obligatorio
    required: bool = True

    # True = requiere IA
    requires_ai: bool = False

    # -------------------------
    # Resultado esperado
    # -------------------------

    severity: str = "MEDIUM"

    recommendation: Optional[str] = None

    # -------------------------
    # Helpers
    # -------------------------

    def applies_to_issue(self, issue_type: str) -> bool:
        """
        Indica si la regla aplica al tipo de Issue.
        """

        return issue_type in self.applies_to

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"