"""
Test Case Generator Agent - CLI Entry Point
"""

from __future__ import annotations

import argparse
import json
from dotenv import load_dotenv

from src.bootstrap.dependency_injection import build_application
from src.domain.entities import AcceptanceCriterion, UserStory, GenerationOptions

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Test Case Generator Agent CLI")
    parser.add_argument("--project", required=True, help="Clave del proyecto (ej. GES)")
    parser.add_argument("--issue", required=True, help="Clave del Issue/Historia (ej. GES-123)")
    parser.add_argument("--story", required=True, help="Texto de la Historia de Usuario")
    parser.add_argument("--criteria", nargs="*", default=[], help="Criterios de aceptación")

    args = parser.parse_args()

    story = UserStory(
        project_key=args.project,
        issue_key=args.issue,
        raw_text=args.story,
    )

    criteria = [
        AcceptanceCriterion(id=f"AC-{i+1:03d}", description=c)
        for i, c in enumerate(args.criteria)
    ]

    use_case = build_application()
    result = use_case.execute(story=story, criteria=criteria, options=GenerationOptions())

    print("\n=======================================================")
    print("TEST CASE GENERATOR AGENT - RESULTADOS")
    print("=======================================================")
    print(f"Proyecto      : {result.project_key}")
    print(f"Issue         : {result.issue_key}")
    print(f"Casos Totales : {result.total_cases}")
    print(f"  Positivos   : {result.positive_count}")
    print(f"  Negativos   : {result.negative_count}")
    print(f"  Validación  : {result.validation_count}")
    print(f"  Límites     : {result.boundary_count}")
    print(f"Trazabilidad  : {result.traceability_rate}%")
    print(f"Confianza     : {result.overall_confidence.value}")
    print("=======================================================\n")

    for tc in result.test_cases:
        print(f"[{tc.id}] {tc.title} ({tc.type.value} | {tc.priority.value})")
        print(f"  Criterio : {tc.acceptance_criteria_reference or 'USER_STORY'}")
        print(f"  Esperado : {tc.expected_result}\n")


if __name__ == "__main__":
    main()
