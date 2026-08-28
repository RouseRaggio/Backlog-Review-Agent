"""
Unit Tests for RuleBasedTestCaseGenerator - Strict No-Invention & Evidence Tests.
"""

from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    UserStory,
)
from src.domain.enums import Confidence, Priority, TestCaseType
from src.infrastructure.generators.rule_based_generator import RuleBasedTestCaseGenerator


def test_generator_no_invention_on_simple_crud():
    """
    CRITICAL TEST:
    Given: 'El administrador puede crear un usuario.'
    The generator MUST NOT create cases for:
    - invalid email
    - duplicate email
    - empty name
    - invalid role
    - maximum length
    """
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Administrador quiero gestionar usuarios para controlar acceso.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-001", description="El administrador puede crear un usuario.")
    ]

    generator = RuleBasedTestCaseGenerator()
    cases = generator.generate(story, criteria, GenerationOptions())

    # Only 1 positive case should be generated
    assert len(cases) == 1
    assert cases[0].type == TestCaseType.POSITIVE

    # Verify no invented negative cases exist
    titles_and_descriptions = " ".join([c.title + " " + c.description for c in cases]).lower()
    assert "email" not in titles_and_descriptions
    assert "duplicado" not in titles_and_descriptions
    assert "longitud" not in titles_and_descriptions
    assert "caracteres" not in titles_and_descriptions
    assert "vacío" not in titles_and_descriptions


def test_generator_uniqueness_negative_case():
    """
    Given: 'El sistema valida que el correo electrónico sea único.'
    The generator MAY create a duplicate-email validation case.
    """
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Administrador quiero registrar usuarios.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-002", description="El sistema valida que el correo electrónico sea único.")
    ]

    generator = RuleBasedTestCaseGenerator()
    cases = generator.generate(story, criteria, GenerationOptions())

    negative_cases = [c for c in cases if c.type == TestCaseType.NEGATIVE]
    assert len(negative_cases) == 1
    assert "duplicado" in negative_cases[0].title.lower() or "duplicado" in negative_cases[0].description.lower()
    assert negative_cases[0].acceptance_criteria_reference == "AC-002"
    assert negative_cases[0].priority == Priority.CRITICAL


def test_generator_boundary_cases_on_explicit_limits():
    """
    Given: 'El nombre debe tener entre 3 y 50 caracteres.'
    The generator MAY create boundary cases for 3, 50, 2, 51.
    """
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Usuario quiero registrar mi perfil.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-003", description="El nombre debe tener entre 3 y 50 caracteres.")
    ]

    generator = RuleBasedTestCaseGenerator()
    cases = generator.generate(story, criteria, GenerationOptions())

    boundary_cases = [c for c in cases if c.type == TestCaseType.BOUNDARY]
    assert len(boundary_cases) == 4

    boundary_texts = " ".join([c.title + " " + c.description for c in boundary_cases])
    assert "3" in boundary_texts
    assert "50" in boundary_texts
    assert "2" in boundary_texts
    assert "51" in boundary_texts


def test_generator_no_boundary_cases_when_no_limits():
    """
    When no explicit numbers/limits exist, no boundary cases should be generated.
    """
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Usuario quiero enviar comentarios.",
    )
    criteria = [
        AcceptanceCriterion(id="AC-001", description="El usuario puede enviar un comentario.")
    ]

    generator = RuleBasedTestCaseGenerator()
    cases = generator.generate(story, criteria, GenerationOptions())

    boundary_cases = [c for c in cases if c.type == TestCaseType.BOUNDARY]
    assert len(boundary_cases) == 0


def test_generator_without_acceptance_criteria():
    """
    Without criteria, generates preliminary case with LOW confidence and REVIEW_REQUIRED.
    """
    story = UserStory(
        project_key="GES",
        issue_key="GES-123",
        raw_text="Como Administrador quiero gestionar documentos para organizar archivos.",
    )

    generator = RuleBasedTestCaseGenerator()
    cases = generator.generate(story, [], GenerationOptions())

    assert len(cases) == 1
    assert cases[0].confidence == Confidence.LOW
    assert cases[0].acceptance_criteria_reference is None
