"""
Presentation Mappers.

Transforma entidades de dominio (AuditReport, Finding)
a DTOs de presentación (ReviewResponse, FindingDTO).
"""

from __future__ import annotations

from src.domain.entities.audit_report import AuditReport
from src.domain.entities.finding import Finding
from src.presentation.api.schemas import (
    FindingDTO,
    ProjectDTO,
    ReviewResponse,
    StatisticsDTO,
)


def map_finding_to_dto(finding: Finding) -> FindingDTO:
    """
    Convierte un Finding de dominio a FindingDTO.
    """
    return FindingDTO(
        rule_id=finding.rule_id,
        rule_name=finding.rule_name,
        issue_key=finding.issue_key,
        issue_type=finding.issue_type,
        status=finding.status,
        severity=finding.severity,
        message=finding.message,
        recommendation=finding.recommendation,
    )


def map_audit_report_to_response(report: AuditReport) -> ReviewResponse:
    """
    Convierte un AuditReport de dominio a ReviewResponse DTO.

    Calcula `total_issues` a partir del conjunto único de issue_keys
    en los findings, diferenciándolo de `total_findings`.
    """
    unique_issue_keys = {finding.issue_key for finding in report.findings}
    total_issues = len(unique_issue_keys)

    statistics = StatisticsDTO(
        total_issues=total_issues,
        total_findings=report.total_findings,
        passed=report.passed,
        warnings=report.warnings,
        failed=report.failed,
        blocked=report.blocked,
    )

    project = ProjectDTO(
        key=report.project_key,
        name=report.project_name,
    )

    finding_dtos = [map_finding_to_dto(f) for f in report.findings]

    return ReviewResponse(
        project=project,
        quality_score=report.quality_score,
        statistics=statistics,
        findings=finding_dtos,
    )
