"""
Integration / Unit Test simulating the real Jira structure of GES-70.
"""

from src.infrastructure.jira.criteria_extractor import CriteriaExtractor
from src.infrastructure.jira.jira_gateway_adapter import JiraGatewayAdapter
from src.application.use_cases.analyze_user_story import AnalyzeUserStoryUseCase
from src.application.use_cases.generate_test_cases import GenerateTestCasesUseCase
from src.infrastructure.generators.rule_based_generator import RuleBasedTestCaseGenerator
from src.domain.enums import Confidence
from unittest.mock import MagicMock


def test_ges70_extraction_and_analysis():
    # 1. Mock de los campos reales de Jira para GES-70
    mock_fields = {
        "summary": "Gestión y radicación de comunicaciones oficiales",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Como usuario autorizado del SGDEA quiero registrar y radicar comunicaciones oficiales de entrada, salida e internas para generar un número de radicación único."}
                    ]
                }
            ]
        },
        "customfield_10614": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "bulletList",
                    "content": [
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El usuario puede registrar comunicaciones de entrada, salida e internas."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El sistema genera automáticamente el código de radicación."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El consecutivo es único e irrepetible."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El consecutivo se administra correctamente por tipo de comunicación."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El sistema registra automáticamente la fecha y hora de radicación."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "La comunicación queda asociada al expediente correspondiente."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "La comunicación queda asociada a la serie y subserie documental."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "El sistema calcula correctamente los tiempos de respuesta."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Solo usuarios autorizados pueden radicar comunicaciones."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Todas las operaciones quedan registradas en la auditoría."}]}]}
                    ]
                }
            ]
        },
        "customfield_10615": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "bulletList",
                    "content": [
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Registro de comunicación de entrada."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Registro de comunicación de salida."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Registro de comunicación interna."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación del consecutivo único."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación del reinicio anual del consecutivo."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación de asociación al expediente electrónico."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación de asociación a series y subseries."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación de tiempos de respuesta."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación de permisos."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Validación de auditoría."}]}]},
                        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Pruebas funcionales de extremo a extremo."}]}]}
                    ]
                }
            ]
        },
        "issuetype": {"name": "Historia"},
        "priority": {"name": "Muy Alta"},
        "status": {"name": "En curso"},
        "assignee": {"displayName": "Hector Garcia"}
    }

    mock_client = MagicMock()
    mock_client.get_issue.return_value = {
        "id": "71031",
        "key": "GES-70",
        "fields": mock_fields,
    }

    adapter = JiraGatewayAdapter(client=mock_client)
    analyze_uc = AnalyzeUserStoryUseCase(jira_gateway=adapter)

    # 2. Ejecutar análisis
    analysis = analyze_uc.execute(project_key="GESTADOC", issue_key="GES-70")

    # 3. Verificaciones rigurosas
    assert analysis.issue_key == "GES-70"
    assert len(analysis.criteria) == 10, f"Se esperaban 10 criterios, se obtuvieron {len(analysis.criteria)}"
    assert len(analysis.qa_tests) == 11, f"Se esperaban 11 pruebas QA, se obtuvieron {len(analysis.qa_tests)}"

    # Verificar que los criterios tienen IDs asignados
    assert analysis.criteria[0].id == "AC-001"
    assert "registrar comunicaciones" in analysis.criteria[0].description
    assert analysis.criteria[9].id == "AC-010"
    assert "auditoría" in analysis.criteria[9].description

    # Verificar que las pruebas QA están separadas
    assert "Registro de comunicación de entrada." in analysis.qa_tests
    assert "Pruebas funcionales de extremo a extremo." in analysis.qa_tests

    # Verificar suficiencia y ausencia de warnings
    assert analysis.sufficient_information is True
    assert analysis.confidence == Confidence.HIGH
    assert not any("no fueron proporcionados" in w for w in analysis.warnings)

    # 4. Generación de Test Cases a partir de los 10 criterios
    gen_uc = GenerateTestCasesUseCase(
        generator=RuleBasedTestCaseGenerator(),
        jira_gateway=adapter,
    )
    result = gen_uc.execute(project_key="GESTADOC", issue_key="GES-70")

    # Debe generar múltiples casos de prueba a partir de los criterios reales
    assert result.total_cases >= 10, f"Se esperaban al menos 10 casos de prueba, se obtuvieron {result.total_cases}"
    assert result.positive_count >= 5
    assert result.traceability_rate == 100.0
    assert result.overall_confidence == Confidence.HIGH
