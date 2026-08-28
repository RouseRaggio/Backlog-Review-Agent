from src.domain.entities.audit_report import AuditReport
from src.domain.entities.finding import Finding
from src.presentation.html.html_report_generator import HtmlReportGenerator

findings = [
    Finding(rule_id="BR-001", rule_name="Missing Issue Title", issue_key="PROJ-101", issue_type="Story", status="FAIL", severity="CRITICAL", message="Title is missing", recommendation="Add a descriptive title"),
    Finding(rule_id="BR-002", rule_name="Story has no Description", issue_key="PROJ-101", issue_type="Story", status="FAIL", severity="HIGH", message="No description", recommendation="Add a description"),
    Finding(rule_id="BR-003", rule_name="Priority not assigned", issue_key="PROJ-101", issue_type="Story", status="FAIL", severity="MEDIUM", message="No priority", recommendation="Assign priority"),
    Finding(rule_id="BR-004", rule_name="No Assignee assigned", issue_key="PROJ-102", issue_type="Bug", status="FAIL", severity="HIGH", message="No assignee", recommendation="Assign to a team member"),
    Finding(rule_id="BR-005", rule_name="Not associated to a Sprint", issue_key="PROJ-102", issue_type="Bug", status="WARNING", severity="LOW", message="Not in sprint", recommendation="Add to current sprint"),
    Finding(rule_id="BR-006", rule_name="Not associated to an Epic", issue_key="PROJ-103", issue_type="Task", status="PASS", severity=None, message="Epic linked", recommendation=None),
    Finding(rule_id="BR-007", rule_name="Story Points not defined", issue_key="PROJ-103", issue_type="Task", status="BLOCKED", severity="CRITICAL", message="No story points", recommendation="Estimate story points"),
    Finding(rule_id="BR-008", rule_name="Missing Acceptance Criteria", issue_key="PROJ-104", issue_type="Story", status="FAIL", severity="MEDIUM", message="No acceptance criteria", recommendation="Define acceptance criteria"),
    Finding(rule_id="BR-009", rule_name="Status not assigned", issue_key="PROJ-104", issue_type="Story", status="PASS", severity=None, message="Status is set", recommendation=None),
    Finding(rule_id="BR-010", rule_name="Issue Type not assigned", issue_key="PROJ-105", issue_type="Epic", status="FAIL", severity="HIGH", message="No issue type", recommendation="Assign issue type"),
    Finding(rule_id="BR-001", rule_name="Missing Issue Title", issue_key="PROJ-105", issue_type="Epic", status="FAIL", severity="LOW", message="Title issue", recommendation="Fix title"),
    Finding(rule_id="BR-004", rule_name="No Assignee assigned", issue_key="PROJ-106", issue_type="Bug", status="PASS", severity=None, message="Assignee present", recommendation=None),
]

report = AuditReport(
    project_key="TEST",
    project_name="Test Project",
    findings=findings,
    quality_score=68.5,
)

generator = HtmlReportGenerator()
path = generator.generate(report)
print(f"Report generated: {path.resolve()}")
