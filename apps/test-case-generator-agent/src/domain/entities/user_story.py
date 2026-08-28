"""
Domain Entity: UserStory
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class UserStory:
    """
    Representa una Historia de Usuario en el dominio.
    """

    project_key: str
    issue_key: str
    raw_text: str
    title: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    benefit: Optional[str] = None

    def __post_init__(self):
        if not self.role or not self.goal:
            self._extract_standard_format()

    def _extract_standard_format(self) -> None:
        """
        Intenta extraer Rol, Objetivo y Beneficio del texto en formato estándar:
        'Como [rol] quiero [objetivo] para [beneficio]'
        """
        text = self.raw_text.strip()
        lower = text.lower()

        if "como " in lower:
            como_idx = lower.find("como ") + 5
            quiero_idx = lower.find(" quiero ")
            para_idx = lower.find(" para ")

            if quiero_idx != -1:
                self.role = text[como_idx:quiero_idx].strip()
                if para_idx != -1 and para_idx > quiero_idx:
                    self.goal = text[quiero_idx + 8:para_idx].strip()
                    self.benefit = text[para_idx + 6:].strip()
                else:
                    self.goal = text[quiero_idx + 8:].strip()
            else:
                self.role = "Usuario"
                self.goal = text
        else:
            self.role = "Usuario"
            self.goal = text
