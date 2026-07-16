"""
Test del Rule Engine.

Este archivo permite validar que las reglas automáticas
se ejecutan correctamente sobre un Issue.
"""

from src.domain.models.issue import Issue
from src.domain.services.rule_engine import RuleEngine


def main():

    issue = Issue(
        id="10001",
        key="CAP-249",

        issue_type="Historia",

        summary="Acta de reunión posesión docente",

        description="",

        priority=None,

        status="To Do",

        reporter="Rouse",

        assignee=None,

        epic=None,

        sprint="Sprint 81",

        story_points=None,

        acceptance_criteria=None,

        labels=[],

        url="https://developapp.atlassian.net/browse/CAP-249",
    )

    engine = RuleEngine()

    findings = engine.evaluate(issue)

    print("\n===========================================")
    print("RESULTADO AUDITORÍA")
    print("===========================================\n")

    print(f"Issue : {issue.key}")
    print(f"Tipo  : {issue.issue_type}")
    print(f"Título: {issue.summary}")

    print("\nHallazgos\n")

    for finding in findings:

        print("---------------------------------------")
        print(f"Regla      : {finding.rule_id}")
        print(f"Nombre     : {finding.rule_name}")
        print(f"Estado     : {finding.status}")
        print(f"Severidad  : {finding.severity}")
        print(f"Mensaje    : {finding.message}")

        if finding.recommendation:
            print(f"Recomendación: {finding.recommendation}")

    print("\n===========================================\n")


if __name__ == "__main__":
    main()