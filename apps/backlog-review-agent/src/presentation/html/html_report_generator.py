"""
HTML Report Generator

Genera un reporte HTML a partir de un AuditReport.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.domain.entities.audit_report import AuditReport


class HtmlReportGenerator:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent

        self.template_path = (
            base_dir
            / "templates"
            / "report.html"
        )

        print("Template:", self.template_path)
        print("Existe:", self.template_path.exists())

        self.output_dir = Path("reports/latest")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

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

            rows.append(
                f"""
<tr data-status="{finding.status}" data-severity="{severity}">

<td>{finding.issue_key}</td>

<td>{finding.rule_id}</td>

<td>{badge}</td>

<td>{severity}</td>

<td>{finding.message}</td>

<td>{finding.recommendation or "-"}</td>

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