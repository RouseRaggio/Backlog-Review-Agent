"""
Unit Tests for SufficiencyValidator.
"""

import pytest
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    UserStory,
)
from src.domain.enums import Confidence
from src.domain.services.sufficiency_validator import SufficiencyValidator


def test_sufficiency_empty_story_raises_value_error():
    validator = SufficiencyValidator()
    story = UserStory(project_key="GES", issue_key="GES-1", raw_text="   ")
    with pytest.raises(ValueError):
        validator.validate(story, [], GenerationOptions())


def test_sufficiency_missing_criteria_adds_warning_and_low_confidence():
    validator = SufficiencyValidator()
    story = UserStory(project_key="GES", issue_key="GES-1", raw_text="Como usuario quiero ver mi perfil.")
    warnings, confidence = validator.validate(story, [], GenerationOptions())

    assert confidence == Confidence.LOW
    assert any("criterios de aceptación no fueron proporcionados" in w for w in warnings)


def test_sufficiency_missing_boundary_adds_warning():
    validator = SufficiencyValidator()
    story = UserStory(project_key="GES", issue_key="GES-1", raw_text="Como usuario quiero enviar un mensaje.")
    criteria = [AcceptanceCriterion(id="AC-001", description="El usuario puede enviar un mensaje.")]
    warnings, confidence = validator.validate(story, criteria, GenerationOptions(include_boundary=True))

    assert confidence == Confidence.HIGH
    assert any("No se generaron casos límite" in w for w in warnings)
