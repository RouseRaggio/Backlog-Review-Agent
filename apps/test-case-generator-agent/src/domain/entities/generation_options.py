"""
Domain Entity: GenerationOptions
"""

from __future__ import annotations

from dataclasses import dataclass
from src.domain.enums import Priority


@dataclass(slots=True)
class GenerationOptions:
    """
    Opciones de configuración para la generación de casos de prueba.
    """

    include_positive: bool = True
    include_negative: bool = True
    include_validation: bool = True
    include_boundary: bool = True
    detail_level: str = "standard"  # "basic", "standard", "detailed"
    min_priority: Priority = Priority.LOW
