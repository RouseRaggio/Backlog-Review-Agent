"""
Domain Entity: AcceptanceCriterion
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class AcceptanceCriterion:
    """
    Representa un Criterio de Aceptación individual.
    """

    id: str
    description: str
    rule_type: Optional[str] = None
    is_negative: bool = False
