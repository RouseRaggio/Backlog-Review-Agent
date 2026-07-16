"""
Backlog Review Agent

Punto de entrada de la aplicación.
"""

from __future__ import annotations

import argparse
import webbrowser

from src.presentation.html.html_report_generator import (
    HtmlReportGenerator,
)

from src.use_cases.audit_backlog import AuditBacklogUseCase
from src.domain.services.rule_engine import RuleEngine
from src.domain.services.score_service import ScoreService
from src.infrastructure.jira.jira_client import JiraClient


def build_application() -> AuditBacklogUseCase:
    """
    Construye las dependencias de la aplicación.
    """

    jira_client = JiraClient()

    rule_engine = RuleEngine()

    score_service = ScoreService()

    return AuditBacklogUseCase(
        jira_client=jira_client,
        rule_engine=rule_engine,
        score_service=score_service,
    )


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Backlog Review Agent"
    )

    parser.add_argument(
        "--project",
        required=True,
        help="Clave del proyecto Jira",
    )

    parser.add_argument(
        "--max-results",
        default=100,
        type=int,
        help="Cantidad máxima de Issues",
    )

    return parser.parse_args()


def print_summary(report):

    print()

    print("=" * 60)

    print("BACKLOG REVIEW AGENT")

    print("=" * 60)

    print()

    print(f"Proyecto            : {report.project_key}")

    print(f"Hallazgos           : {report.total_findings}")

    print(f"PASS                : {report.passed}")

    print(f"WARNING             : {report.warnings}")

    print(f"FAIL                : {report.failed}")

    print(f"BLOCKED             : {report.blocked}")

    print()

    print(f"Backlog Score       : {report.quality_score}%")

    print()

    print("=" * 60)


def main():

    args = parse_arguments()

    application = build_application()

    report = application.execute(
        project_key=args.project,
        max_results=args.max_results,
    )
    generator = HtmlReportGenerator()

    report_path = generator.generate(report)

    print(f"\nReporte generado:\n{report_path}")

    webbrowser.open(
        report_path.resolve().as_uri()
    )




if __name__ == "__main__":
    main()