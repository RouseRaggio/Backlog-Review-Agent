"""
Domain Service: SufficiencyValidator
"""

from __future__ import annotations

import re
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    UserStory,
)
from src.domain.enums import Confidence


class SufficiencyValidator:
    """
    Evalúa la suficiencia de información en la entrada y determina advertencias y nivel de confianza.
    """

    BOUNDARY_PATTERN = re.compile(
        r"(\b\d+\b|entre\s+\d+|m[áa]ximo|m[íi]nimo|l[íi]mite|rango|hasta\s+\d+|mayor\s+que|menor\s+que)",
        re.IGNORECASE,
    )

    def validate(
        self,
        story: UserStory,
        criteria: list[AcceptanceCriterion],
        options: GenerationOptions,
    ) -> tuple[list[str], Confidence]:
        """
        Retorna (lista de advertencias, confianza base).
        """
        warnings: list[str] = []
        confidence = Confidence.HIGH

        if not story.raw_text.strip():
            raise ValueError("El texto de la Historia de Usuario no puede estar vacío.")

        # 1. Validación de Criterios de Aceptación
        if not criteria:
            warnings.append(
                "Los criterios de aceptación no fueron proporcionados. Los casos generados son preliminares y requieren revisión."
            )
            confidence = Confidence.LOW

        # 2. Validación de Límites (Boundary)
        if options.include_boundary:
            has_boundary_info = self._has_boundary_evidence(story, criteria)
            if not has_boundary_info:
                warnings.append(
                    "No se generaron casos límite porque la Historia de Usuario y los criterios de aceptación no especifican valores límite o umbrales."
                )

        return warnings, confidence

    def _has_boundary_evidence(
        self,
        story: UserStory,
        criteria: list[AcceptanceCriterion],
    ) -> bool:
        """
        Comprueba si existe evidencia explícita de valores numéricos, rangos o umbrales.
        """
        if self.BOUNDARY_PATTERN.search(story.raw_text):
            return True

        for ac in criteria:
            if self.BOUNDARY_PATTERN.search(ac.description):
                return True

        return False
