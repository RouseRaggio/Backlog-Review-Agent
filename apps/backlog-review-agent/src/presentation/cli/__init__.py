"""
CLI Controller: Argumentos y presentación en consola.
"""

from __future__ import annotations

import argparse


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
