"""
Domain Service: TraceabilityService
"""

from __future__ import annotations

from src.domain.entities import AcceptanceCriterion, TestCase


class TraceabilityService:
    """
    Construye la matriz de trazabilidad entre Criterios de Aceptación y Casos de Prueba.
    """

    def build_traceability_map(
        self,
        criteria: list[AcceptanceCriterion],
        test_cases: list[TestCase],
    ) -> dict[str, list[str]]:
        """
        Retorna un diccionario {ac_id: [test_case_id, ...]}.
        Si no hay criterios, agrupa bajo 'USER_STORY'.
        """
        if not criteria:
            return {
                "USER_STORY": [tc.id for tc in test_cases],
            }

        traceability_map: dict[str, list[str]] = {ac.id: [] for ac in criteria}

        for tc in test_cases:
            ac_ref = tc.acceptance_criteria_reference
            if ac_ref and ac_ref in traceability_map:
                traceability_map[ac_ref].append(tc.id)
            elif ac_ref:
                if ac_ref not in traceability_map:
                    traceability_map[ac_ref] = []
                traceability_map[ac_ref].append(tc.id)

        return traceability_map
