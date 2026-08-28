"""
Unit Tests for AnalyzeUserStoryUseCase and GenerateTestCasesUseCase with Jira Gateway.
"""

from unittest.mock import MagicMock
import pytest

from src.application.use_cases.analyze_user_story import AnalyzeUserStoryUseCase
from src.application.use_cases.generate_test_cases import GenerateTestCasesUseCase
from src.domain.entities import AcceptanceCriterion, GenerationOptions, UserStory
from src.domain.enums import Confidence
from src.domain.services.jira_gateway import JiraGateway, UserStoryNotFoundError
from src.infrastructure.generators.rule_based_generator import RuleBasedTestCaseGenerator


class MockJiraGateway(JiraGateway):
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def get_user_story(self, project_key: str, issue_key: str):
        if self.should_fail:
            raise UserStoryNotFoundError(f"Issue {issue_key} no encontrada.")
        story = UserStory(
            project_key=project_key,
            issue_key=issue_key,
            title="Gestión de accesos",
            raw_text="Como admin quiero gestionar accesos para seguridad.",
        )
        criteria = [
            AcceptanceCriterion(id="AC-001", description="El admin puede crear un nuevo usuario con rol."),
            AcceptanceCriterion(id="AC-002", description="El sistema valida que el correo sea único."),
        ]
        qa_tests = [
            "Prueba de creación de usuario.",
            "Validación de correo único.",
        ]
        metadata = {"priority": "High", "status": "Ready"}
        return story, criteria, qa_tests, metadata



def test_analyze_user_story_use_case_success():
    gateway = MockJiraGateway()
    use_case = AnalyzeUserStoryUseCase(jira_gateway=gateway)

    result = use_case.execute(project_key="GES", issue_key="GES-40")

    assert result.project_key == "GES"
    assert result.issue_key == "GES-40"
    assert len(result.criteria) == 2
    assert result.source == "jira"
    assert result.sufficient_information is True
    assert result.confidence == Confidence.HIGH


def test_analyze_user_story_use_case_not_found():
    gateway = MockJiraGateway(should_fail=True)
    use_case = AnalyzeUserStoryUseCase(jira_gateway=gateway)

    with pytest.raises(UserStoryNotFoundError):
        use_case.execute(project_key="GES", issue_key="NONEXIST-999")


def test_generate_test_cases_via_jira_gateway():
    gateway = MockJiraGateway()
    generator = RuleBasedTestCaseGenerator()
    use_case = GenerateTestCasesUseCase(generator=generator, jira_gateway=gateway)

    result = use_case.execute(project_key="GES", issue_key="GES-40")

    assert result.project_key == "GES"
    assert result.issue_key == "GES-40"
    assert result.total_cases > 0
    assert result.traceability_rate == 100.0


def test_generate_test_cases_manual_fallback():
    gateway = MockJiraGateway(should_fail=True)  # Should not be called
    generator = RuleBasedTestCaseGenerator()
    use_case = GenerateTestCasesUseCase(generator=generator, jira_gateway=gateway)

    manual_story = UserStory(
        project_key="MANUAL",
        issue_key="MAN-01",
        raw_text="Como usuario quiero iniciar sesión con credenciales válidas.",
    )
    manual_criteria = [
        AcceptanceCriterion(id="AC-001", description="Ingresar email y contraseña correctos."),
    ]

    result = use_case.execute(
        story=manual_story,
        criteria=manual_criteria,
    )

    assert result.project_key == "MANUAL"
    assert result.issue_key == "MAN-01"
    assert result.total_cases > 0
