"""
HTML Report Generator

Genera un reporte HTML a partir de un AuditReport.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.domain.entities.audit_report import AuditReport

RULE_DESCRIPTIONS = {
    "BR-001": "Missing Issue Title",
    "BR-002": "Story has no Description",
    "BR-003": "Priority not assigned",
    "BR-004": "No Assignee assigned",
    "BR-005": "Not associated to a Sprint",
    "BR-006": "Not associated to an Epic",
    "BR-007": "Story Points not defined",
    "BR-008": "Missing Acceptance Criteria",
    "BR-009": "Status not assigned",
    "BR-010": "Issue Type not assigned",
}


class HtmlReportGenerator:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent

        self.template_path = (
            base_dir
            / "templates"
            / "report.html"
        )

        self.chartjs_path = (
            base_dir
            / "templates"
            / "chart.min.js"
        )

        self.output_dir = Path("reports/latest")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _read_chartjs(self) -> str:
        return self.chartjs_path.read_text(encoding="utf-8")

    def generate(self, report: AuditReport) -> Path:
        """
        Genera el reporte HTML.

        Parameters
        ----------
        report : AuditReport

        Returns
        -------
        Path
        """

        template = self.template_path.read_text(
            encoding="utf-8"
        )

        template = template.replace(
            "{{PROJECT}}",
            report.project_key,
        )

        template = template.replace(
            "{{DATE}}",
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

        template = template.replace(
            "{{SCORE}}",
            f"{report.quality_score:.2f}",
        )

        total_issues = len(
            {f.issue_key for f in report.findings}
        )

        template = template.replace(
            "{{ISSUES_TOTAL}}",
            str(total_issues),
        )

        template = template.replace(
            "{{TOTAL}}",
            str(report.total_findings),
        )

        template = template.replace(
            "{{PASS}}",
            str(report.passed),
        )

        template = template.replace(
            "{{FAIL}}",
            str(report.failed),
        )

        template = template.replace(
            "{{WARNING}}",
            str(report.warnings),
        )

        template = template.replace(
            "{{BLOCKED}}",
            str(report.blocked),
        )

        template = template.replace(
            "{{FINDINGS}}",
            self._build_findings(report),
        )

        template = template.replace(
            "{{CHARTJS}}",
            self._read_chartjs(),
        )

        output_file = (
            self.output_dir /
            f"{report.project_key}_AUDIT.html"
        )

        output_file.write_text(
            template,
            encoding="utf-8",
        )

        return output_file

    def _build_findings(
        self,
        report: AuditReport,
    ) -> str:

        rows = []

        for finding in report.findings:

            badge = self._status_badge(
                finding.status
            )

            severity = finding.severity or "-"

            sev_badge = self._severity_badge(severity)

            rule_desc = RULE_DESCRIPTIONS.get(
                finding.rule_id, finding.rule_name
            )

            if finding.status == "FAIL":
                display_desc = f"\u274c {rule_desc}"
            elif finding.status == "WARNING":
                display_desc = f"\u26a0\ufe0f {rule_desc}"
            elif finding.status == "BLOCKED":
                display_desc = f"\u26d4 {rule_desc}"
            else:
                display_desc = f"\u2705 {rule_desc}"

            rows.append(
                f"""
<tr data-status="{finding.status}" data-severity="{severity}" data-rule="{finding.rule_id}" data-issue="{finding.issue_key}" data-issue-type="{finding.issue_type}" data-rule-desc="{rule_desc}">

<td class="col-issue"><span class="issue-key">{finding.issue_key}</span></td>

<td class="col-type"><span class="issue-type-badge">{finding.issue_type}</span></td>

<td class="col-status">{badge}</td>

<td class="col-severity">{sev_badge}</td>

<td class="col-rule">{display_desc}</td>

<td class="col-rec">{finding.recommendation or "-"}</td>

</tr>
"""
            )

        return "\n".join(rows)

    @staticmethod
    def _status_badge(status: str) -> str:

        css = {
            "PASS": "badge badge-pass",
            "FAIL": "badge badge-fail",
            "WARNING": "badge badge-warning",
            "BLOCKED": "badge badge-blocked",
        }.get(status, "badge")

        return (
            f'<span class="{css}">'
            f'{status}'
            f'</span>'
        )

    @staticmethod
    def _severity_badge(severity: str) -> str:

        css_map = {
            "CRITICAL": "sev sev-critical",
            "HIGH": "sev sev-high",
            "MEDIUM": "sev sev-medium",
            "LOW": "sev sev-low",
        }

        css = css_map.get(severity, "sev")

        return (
            f'<span class="{css}">'
            f'{severity}'
            f'</span>'
        )