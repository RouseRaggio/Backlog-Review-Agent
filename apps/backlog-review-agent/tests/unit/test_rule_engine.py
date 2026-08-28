"""
Unit Tests for RuleEngine.
"""

from src.domain.entities.issue import Issue
from src.domain.services.rule_engine import RuleEngine


def test_rule_engine_evaluates_all_passing():
    issue = Issue(
        id="1",
        key="TEST-1",
        issue_type="Historia",
        summary="Valid summary",
        description="Valid description",
        priority="High",
        status="To Do",
        reporter="Tester",
        assignee="Developer",
        epic="EPIC-1",
        sprint="Sprint 1",
        story_points="5",
        acceptance_criteria="Given when then",
        labels=["backend"],
        url="https://jira.example.com/browse/TEST-1",
    )

    engine = RuleEngine()
    findings = engine.evaluate(issue)

    assert len(findings) > 0
    assert all(f.status == "PASS" for f in findings)


def test_rule_engine_detects_failures():
    issue = Issue(
        id="2",
        key="TEST-2",
        issue_type="Historia",
        summary="",
        description="",
        priority=None,
        status="To Do",
        reporter="Tester",
        assignee=None,
        epic=None,
        sprint=None,
        story_points=None,
        acceptance_criteria=None,
        labels=[],
        url="https://jira.example.com/browse/TEST-2",
    )

    engine = RuleEngine()
    findings = engine.evaluate(issue)

    failed_findings = [f for f in findings if f.status == "FAIL"]
    assert len(failed_findings) >= 5
