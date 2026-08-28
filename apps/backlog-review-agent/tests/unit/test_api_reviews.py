"""
Unit Tests for Presentation API (/api/reviews).
"""

from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
import requests

from src.presentation.api.app import create_app
from src.presentation.api.routes import get_audit_use_case
from src.domain.entities.audit_report import AuditReport
from src.domain.entities.finding import Finding
from src.presentation.api.mappers import map_audit_report_to_response, map_finding_to_dto


@pytest.fixture
def mock_use_case():
    return MagicMock()


@pytest.fixture
def client(mock_use_case):
    app = create_app()
    app.dependency_overrides[get_audit_use_case] = lambda: mock_use_case
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backlog-review-agent"}



def test_post_reviews_success(client, mock_use_case):
    """
    Test 1: POST /api/reviews exitoso.
    Verifica que devuelva HTTP 200 y la estructura completa de DTOs.
    """
    # Arrange
    fake_report = AuditReport(project_key="GESTADOC", project_name="Gestión Documental")
    fake_report.quality_score = 83.73
    fake_report.extend([
        Finding(
            rule_id="BR-001",
            rule_name="Missing Issue Title",
            issue_key="GESTADOC-101",
            issue_type="Story",
            status="PASS",
            severity=None,
            message="Regla cumplida.",
            recommendation=None,
        ),
        Finding(
            rule_id="BR-008",
            rule_name="Acceptance Criteria",
            issue_key="GESTADOC-101",
            issue_type="Story",
            status="FAIL",
            severity="HIGH",
            message="No cumple la regla: Acceptance Criteria.",
            recommendation="Definir criterios de aceptación en formato Given-When-Then.",
        ),
        Finding(
            rule_id="BR-001",
            rule_name="Missing Issue Title",
            issue_key="GESTADOC-102",
            issue_type="Bug",
            status="PASS",
            severity=None,
            message="Regla cumplida.",
            recommendation=None,
        ),
    ])
    mock_use_case.execute.return_value = fake_report

    # Act
    response = client.post(
        "/api/reviews",
        json={"project_key": "GESTADOC", "max_results": 50},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["project"]["key"] == "GESTADOC"
    assert data["project"]["name"] == "Gestión Documental"
    assert data["quality_score"] == 83.73

    # Distinción crucial entre total_issues (2 únicas: 101 y 102) y total_findings (3)
    assert data["statistics"]["total_issues"] == 2
    assert data["statistics"]["total_findings"] == 3
    assert data["statistics"]["passed"] == 2
    assert data["statistics"]["failed"] == 1
    assert data["statistics"]["warnings"] == 0
    assert data["statistics"]["blocked"] == 0

    assert len(data["findings"]) == 3
    assert data["findings"][1]["rule_id"] == "BR-008"
    assert data["findings"][1]["issue_key"] == "GESTADOC-101"
    assert data["findings"][1]["status"] == "FAIL"
    assert data["findings"][1]["severity"] == "HIGH"
    assert data["findings"][1]["recommendation"] is not None

    mock_use_case.execute.assert_called_once_with(
        project_key="GESTADOC",
        max_results=50,
    )


def test_post_reviews_invalid_or_empty_project_key(client):
    """
    Test 2: project_key inválido o vacío.
    """
    # Empty string
    response_empty = client.post(
        "/api/reviews",
        json={"project_key": "", "max_results": 100},
    )
    assert response_empty.status_code == 422

    # Whitespace only
    response_ws = client.post(
        "/api/reviews",
        json={"project_key": "   ", "max_results": 100},
    )
    assert response_ws.status_code == 422

    # Missing project_key
    response_missing = client.post(
        "/api/reviews",
        json={"max_results": 100},
    )
    assert response_missing.status_code == 422


def test_post_reviews_invalid_max_results(client):
    """
    Test 3: max_results inválido (<= 0 o no entero).
    """
    # Zero
    response_zero = client.post(
        "/api/reviews",
        json={"project_key": "CAP", "max_results": 0},
    )
    assert response_zero.status_code == 422

    # Negative
    response_neg = client.post(
        "/api/reviews",
        json={"project_key": "CAP", "max_results": -10},
    )
    assert response_neg.status_code == 422

    # String instead of int
    response_str = client.post(
        "/api/reviews",
        json={"project_key": "CAP", "max_results": "invalid"},
    )
    assert response_str.status_code == 422


def test_post_reviews_jira_service_error_handling(client, mock_use_case):
    """
    Test 4: Manejo de error proveniente del servicio Jira.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.text = "Unauthorized"
    mock_use_case.execute.side_effect = requests.exceptions.HTTPError(
        "401 Client Error: Unauthorized",
        response=mock_resp,
    )

    response = client.post(
        "/api/reviews",
        json={"project_key": "PROJ", "max_results": 10},
    )

    assert response.status_code == 502
    data = response.json()
    assert "Credenciales de Jira inválidas o no autorizadas" in data["detail"]


def test_serialization_of_audit_report():
    """
    Test 5: Serialización correcta de AuditReport (DTO mapping).
    """
    report = AuditReport(project_key="TEST", project_name="Test Project")
    report.quality_score = 100.0
    report.add_finding(
        Finding(
            rule_id="BR-001",
            rule_name="Title",
            issue_key="TEST-1",
            issue_type="Story",
            status="PASS",
            severity=None,
            message="OK",
        )
    )
    report.add_finding(
        Finding(
            rule_id="BR-002",
            rule_name="Description",
            issue_key="TEST-1",
            issue_type="Story",
            status="PASS",
            severity=None,
            message="OK",
        )
    )

    response_dto = map_audit_report_to_response(report)

    assert response_dto.project.key == "TEST"
    assert response_dto.project.name == "Test Project"
    assert response_dto.quality_score == 100.0
    assert response_dto.statistics.total_issues == 1  # 1 única issue TEST-1
    assert response_dto.statistics.total_findings == 2
    assert response_dto.statistics.passed == 2
    assert len(response_dto.findings) == 2


def test_serialization_of_finding_statuses_and_severities():
    """
    Test 6: Serialización correcta de Finding con diferentes estados y severidades.
    """
    findings = [
        Finding(
            rule_id="BR-001",
            rule_name="Title",
            issue_key="K-1",
            issue_type="Story",
            status="PASS",
            severity=None,
            message="Passed",
            recommendation=None,
        ),
        Finding(
            rule_id="BR-003",
            rule_name="Priority",
            issue_key="K-2",
            issue_type="Bug",
            status="WARNING",
            severity="LOW",
            message="Warn",
            recommendation="Add priority",
        ),
        Finding(
            rule_id="BR-008",
            rule_name="AC",
            issue_key="K-3",
            issue_type="Story",
            status="FAIL",
            severity="CRITICAL",
            message="Failed",
            recommendation="Add AC",
        ),
        Finding(
            rule_id="BR-009",
            rule_name="Blocked Rule",
            issue_key="K-4",
            issue_type="Story",
            status="BLOCKED",
            severity="HIGH",
            message="Blocked",
            recommendation="Unblock",
        ),
    ]

    for f in findings:
        dto = map_finding_to_dto(f)
        assert dto.rule_id == f.rule_id
        assert dto.rule_name == f.rule_name
        assert dto.issue_key == f.issue_key
        assert dto.issue_type == f.issue_type
        assert dto.status == f.status
        assert dto.severity == f.severity
        assert dto.message == f.message
        assert dto.recommendation == f.recommendation


def test_download_report_success(client, tmp_path, monkeypatch):
    """
    Test 7: Descarga exitosa del reporte HTML.
    Verifica HTTP 200, Content-Type text/html y Content-Disposition filename.
    """
    from pathlib import Path
    reports_dir = Path("reports/latest")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = reports_dir / "DOWNLOADTEST_AUDIT.html"
    report_file.write_text("<html><body>Audit Report</body></html>", encoding="utf-8")

    try:
        response = client.get("/api/reviews/DOWNLOADTEST/report")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert 'filename="DOWNLOADTEST_AUDIT.html"' in response.headers.get("content-disposition", "")
        assert "<html><body>Audit Report</body></html>" in response.text
    finally:
        if report_file.exists():
            report_file.unlink()


def test_download_report_not_found(client):
    """
    Test 8: Reporte inexistente devuelve HTTP 404.
    """
    response = client.get("/api/reviews/NONEXISTENTPROJ999/report")
    assert response.status_code == 404
    data = response.json()
    assert "Reporte no encontrado" in data["detail"]


def test_download_report_invalid_project_key(client):
    """
    Test 9: Clave de proyecto inválida o con caracteres no permitidos devuelve HTTP 400.
    """
    response = client.get("/api/reviews/INVALID!PROJ@/report")
    assert response.status_code == 400
    data = response.json()
    assert "Clave de proyecto inválida" in data["detail"]


def test_download_report_path_traversal_prevention(client):
    """
    Test 10: Intentos de Path Traversal (ej. ../../.env) son bloqueados con HTTP 400 o 404.
    """
    response_dotdot = client.get("/api/reviews/..%2F..%2Fenv/report")
    assert response_dotdot.status_code in (400, 404)

    response_slash = client.get("/api/reviews/..%2Fetc%2Fpasswd/report")
    assert response_slash.status_code in (400, 404)

