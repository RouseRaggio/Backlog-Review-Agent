"""
Unit Tests for Domain Entities of Test Case Generator Agent.
"""

from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    GenerationResult,
    TestCase,
    UserStory,
)
from src.domain.enums import (
    Category,
    Confidence,
    Priority,
    Status,
    TestCaseType,
)


def test_user_story_parsing():
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Administrador quiero gestionar usuarios para mantener el control de accesos.",
    )
    assert story.role == "Administrador"
    assert "gestionar usuarios" in story.goal
    assert "mantener el control" in story.benefit


def test_generation_result_metrics():
    tc1 = TestCase(
        id="TC-001",
        title="Positivo",
        description="Desc",
        type=TestCaseType.POSITIVE,
        category=Category.FUNCTIONAL,
        priority=Priority.HIGH,
        expected_result="OK",
        requirement_reference="GES-123",
        acceptance_criteria_reference="AC-001",
    )
    tc2 = TestCase(
        id="TC-002",
        title="Negativo",
        description="Desc",
        type=TestCaseType.NEGATIVE,
        category=Category.VALIDATION,
        priority=Priority.CRITICAL,
        expected_result="Fail",
        requirement_reference="GES-123",
        acceptance_criteria_reference="AC-002",
    )

    result = GenerationResult(
        project_key="GES",
        issue_key="GES-123",
        test_cases=[tc1, tc2],
        traceability_map={"AC-001": ["TC-001"], "AC-002": ["TC-002"]},
    )

    assert result.total_cases == 2
    assert result.positive_count == 1
    assert result.negative_count == 1
    assert result.validation_count == 0
    assert result.boundary_count == 0
    assert result.traceability_rate == 100.0
