"""
Application Use Case: AnalyzeUserStoryUseCase

Consulta Jira, extrae la Historia de Usuario, sus Criterios de Aceptación y Pruebas QA,
evalúa la suficiencia de información y retorna un diagnóstico previo a la generación.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from src.domain.entities import AcceptanceCriterion, GenerationOptions, UserStory
from src.domain.enums import Confidence
from src.domain.services.jira_gateway import JiraGateway
from src.domain.services.sufficiency_validator import SufficiencyValidator


@dataclass(slots=True)
class AnalysisResult:
    """
    Resultado del análisis de una Historia de Usuario obtenida desde Jira.
    """

    project_key: str
    issue_key: str
    story: UserStory
    criteria: list[AcceptanceCriterion]
    qa_tests: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source: str = "jira"
    sufficient_information: bool = True
    confidence: Confidence = Confidence.HIGH
    warnings: list[str] = field(default_factory=list)


class AnalyzeUserStoryUseCase:
    """
    Caso de uso para analizar la Historia de Usuario antes de generar casos de prueba.
    """

    def __init__(
        self,
        jira_gateway: JiraGateway,
        sufficiency_validator: SufficiencyValidator | None = None,
    ):
        self._jira_gateway = jira_gateway
        self._sufficiency_validator = sufficiency_validator or SufficiencyValidator()

    def execute(
        self,
        project_key: str,
        issue_key: str,
    ) -> AnalysisResult:
        """
        Ejecuta el análisis de la issue de Jira.
        """
        # 1. Obtener desde Jira
        story, criteria, qa_tests, metadata = self._jira_gateway.get_user_story(
            project_key=project_key,
            issue_key=issue_key,
        )

        # 2. Validar suficiencia de información
        warnings, confidence = self._sufficiency_validator.validate(
            story=story,
            criteria=criteria,
            options=GenerationOptions(),
        )

        sufficient = bool((criteria and len(criteria) > 0) or (qa_tests and len(qa_tests) > 0))

        return AnalysisResult(
            project_key=project_key,
            issue_key=issue_key,
            story=story,
            criteria=criteria,
            qa_tests=qa_tests,
            metadata=metadata,
            source="jira",
            sufficient_information=sufficient,
            confidence=confidence,
            warnings=warnings,
        )
