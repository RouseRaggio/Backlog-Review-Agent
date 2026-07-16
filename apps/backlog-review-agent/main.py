"""
Backlog Review Agent

Punto de entrada de la aplicación.
"""

from __future__ import annotations

import webbrowser

from dotenv import load_dotenv

from src.bootstrap.dependency_injection import build_application
from src.presentation.cli import parse_arguments, print_summary
from src.presentation.html.html_report_generator import HtmlReportGenerator

load_dotenv()


def main():

    args = parse_arguments()

    application = build_application()

    report = application.execute(
        project_key=args.project,
        max_results=args.max_results,
    )

    print_summary(report)

    generator = HtmlReportGenerator()

    report_path = generator.generate(report)

    print(f"\nReporte generado:\n{report_path}")

    webbrowser.open(
        report_path.resolve().as_uri()
    )


if __name__ == "__main__":
    main()
