"""
Unit Tests for ScoreService.
"""

from src.domain.entities.audit_report import AuditReport
from src.domain.entities.finding import Finding
from src.domain.services.score_service import ScoreService


def test_score_service_with_no_findings():
    report = AuditReport(project_key="EMPTY")
    service = ScoreService()
    assert service.calculate(report) == 100.0


def test_score_service_calculation():
    report = AuditReport(project_key="TEST")
    report.add_finding(
        Finding(
            rule_id="BR-001",
            rule_name="Title",
            issue_key="T-1",
            issue_type="Story",
            status="PASS",
        )
    )
    report.add_finding(
        Finding(
            rule_id="BR-002",
            rule_name="Description",
            issue_key="T-1",
            issue_type="Story",
            status="FAIL",
        )
    )

    service = ScoreService()
    score = service.calculate(report)
    assert score == 50.0
