"""
Unit Tests for CriteriaExtractor.
"""

from src.infrastructure.jira.criteria_extractor import CriteriaExtractor


def test_extract_criteria_from_numbered_description():
    description = """
    Como administrador quiero gestionar usuarios para mantener el control.

    Criterios de Aceptación:
    1. El usuario administrador puede crear un nuevo usuario con rol.
    2. El sistema valida que el correo sea único.
    3. El sistema muestra un mensaje de confirmación al guardar.
    """
    criteria = CriteriaExtractor.extract(description=description)
    assert len(criteria) == 3
    assert criteria[0].id == "AC-001"
    assert "crear un nuevo usuario" in criteria[0].description
    assert criteria[1].id == "AC-002"
    assert "correo sea único" in criteria[1].description
    assert criteria[2].id == "AC-003"


def test_extract_criteria_from_bullets():
    description = """
    Acceptance Criteria:
    - El usuario debe autenticarse mediante JWT.
    - Las contraseñas deben contener al menos 8 caracteres.
    """
    criteria = CriteriaExtractor.extract(description=description)
    assert len(criteria) == 2
    assert criteria[0].id == "AC-001"
    assert "autenticarse" in criteria[0].description


def test_extract_criteria_from_custom_field():
    custom_field_value = """
    1. Primer criterio desde campo personalizado.
    2. Segundo criterio desde campo personalizado.
    """
    criteria = CriteriaExtractor.extract(
        description="Descripción genérica sin criterios",
        custom_field_value=custom_field_value,
    )
    assert len(criteria) == 2
    assert criteria[0].id == "AC-001"
    assert "Primer criterio" in criteria[0].description


def test_extract_criteria_from_gherkin():
    description = """
    Escenario: Creación exitosa de usuario
    Dado que soy administrador autenticado
    Cuando ingreso los datos válidos del usuario
    Entonces el usuario queda registrado en la base de datos.
    """
    criteria = CriteriaExtractor.extract(description=description)
    assert len(criteria) >= 1
    assert criteria[0].rule_type == "GHERKIN"


def test_extract_empty_when_no_criteria():
    description = "Historia simple sin ningún criterio de aceptación ni viñetas."
    criteria = CriteriaExtractor.extract(description=description)
    assert len(criteria) == 0
