"""
Application Use Case: GenerateTestCasesUseCase

Orquesta el flujo de generación de Casos de Prueba estructurados y trazables:
1. Si no se provee la Historia manualmente, la consulta desde Jira.
2. Valida la suficiencia de información.
3. Invoca el motor de generación (TestCaseGenerator).
4. Construye la matriz de trazabilidad.
5. Consolida métricas y advertencias en un GenerationResult.
"""

from __future__ import annotations

from typing import Optional
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    GenerationResult,
    UserStory,
)
from src.domain.services import (
    JiraGateway,
    SufficiencyValidator,
    TestCaseGenerator,
    TraceabilityService,
)


class GenerateTestCasesUseCase:
    """
    Caso de uso principal para la generación de casos de prueba.
    """

    def __init__(
        self,
        generator: TestCaseGenerator,
        jira_gateway: Optional[JiraGateway] = None,
        sufficiency_validator: Optional[SufficiencyValidator] = None,
        traceability_service: Optional[TraceabilityService] = None,
    ):
        self._generator = generator
        self._jira_gateway = jira_gateway
        self._sufficiency_validator = sufficiency_validator or SufficiencyValidator()
        self._traceability_service = traceability_service or TraceabilityService()

    def execute(
        self,
        story: Optional[UserStory] = None,
        criteria: Optional[list[AcceptanceCriterion]] = None,
        options: Optional[GenerationOptions] = None,
        project_key: Optional[str] = None,
        issue_key: Optional[str] = None,
    ) -> GenerationResult:
        """
        Ejecuta la generación de casos de prueba.
        Soporta modo manual y modo Jira automático.
        """
        opts = options or GenerationOptions()

        # Si no se pasó story manual o su texto está vacío, consultar Jira
        if not story or not story.raw_text.strip():
            p_key = project_key or (story.project_key if story else "")
            i_key = issue_key or (story.issue_key if story else "")

            if not p_key or not i_key:
                raise ValueError("Se requiere 'project_key' e 'issue_key' para consultar Jira.")

            if not self._jira_gateway:
                raise ValueError("JiraGateway no está configurado para consultar Jira automáticamente.")

            story, criteria, qa_tests, _ = self._jira_gateway.get_user_story(
                project_key=p_key,
                issue_key=i_key,
            )
        else:
            criteria = criteria if criteria is not None else []

        # 1. Validar suficiencia de información y obtener advertencias
        warnings, overall_confidence = self._sufficiency_validator.validate(
            story=story,
            criteria=criteria,
            options=opts,
        )

        # 2. Generar casos de prueba mediante el motor
        test_cases = self._generator.generate(
            story=story,
            criteria=criteria,
            options=opts,
        )

        # 3. Construir matriz de trazabilidad
        traceability_map = self._traceability_service.build_traceability_map(
            criteria=criteria,
            test_cases=test_cases,
        )

        # 4. Consolidar resultado
        return GenerationResult(
            project_key=story.project_key,
            issue_key=story.issue_key,
            test_cases=test_cases,
            warnings=warnings,
            traceability_map=traceability_map,
            overall_confidence=overall_confidence,
        )
