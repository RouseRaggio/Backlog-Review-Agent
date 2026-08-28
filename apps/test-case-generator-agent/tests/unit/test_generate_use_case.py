"""
Unit Tests for GenerateTestCasesUseCase.
"""

from src.application.use_cases.generate_test_cases import GenerateTestCasesUseCase
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    UserStory,
)
from src.infrastructure.generators.rule_based_generator import RuleBasedTestCaseGenerator


def test_use_case_complete_generation():
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como administrador del sistema quiero gestionar los usuarios para mantener el control sobre el acceso y los permisos.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-001", description="El administrador puede crear un usuario proporcionando nombre, correo electrónico y rol."),
        AcceptanceCriterion(id="AC-002", description="El sistema valida que el correo electrónico sea único."),
        AcceptanceCriterion(id="AC-003", description="El administrador puede asignar roles al usuario."),
        AcceptanceCriterion(id="AC-004", description="El sistema muestra un mensaje de éxito al crear el usuario."),
        AcceptanceCriterion(id="AC-005", description="El administrador puede desactivar un usuario existente."),
    ]

    use_case = GenerateTestCasesUseCase(generator=RuleBasedTestCaseGenerator())
    result = use_case.execute(story=story, criteria=criteria, options=GenerationOptions())

    assert result.project_key == "GES"
    assert result.issue_key == "GES-123"
    assert result.total_cases >= 5
    assert result.positive_count >= 3
    assert result.negative_count >= 1
    assert result.traceability_rate == 100.0
    assert "AC-001" in result.traceability_map
    assert "AC-002" in result.traceability_map
