"""
Presentation API Schemas / DTOs.

Separa los modelos de dominio de las estructuras de transporte HTTP.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ReviewRequest(BaseModel):
    """
    Parámetros de entrada para iniciar una revisión de Backlog.
    """

    project_key: str = Field(
        ...,
        description="Clave del proyecto Jira (ej. GESTADOC, CAP)",
        examples=["GESTADOC"],
    )
    max_results: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Número máximo de Issues a recuperar y auditar",
        examples=[100],
    )

    @field_validator("project_key")
    @classmethod
    def validate_project_key(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not cleaned:
            raise ValueError("project_key no puede estar vacío")
        return cleaned


class ProjectDTO(BaseModel):
    """
    Información del proyecto auditado.
    """

    key: str
    name: Optional[str] = None


class StatisticsDTO(BaseModel):
    """
    Resumen cuantitativo de la auditoría.
    Distingue total_issues de total_findings.
    """

    total_issues: int
    total_findings: int
    passed: int
    warnings: int
    failed: int
    blocked: int


class FindingDTO(BaseModel):
    """
    Detalle de un hallazgo generado por una regla de auditoría.
    """

    rule_id: str
    rule_name: str
    issue_key: str
    issue_type: str
    status: str
    severity: Optional[str] = None
    message: str = ""
    recommendation: Optional[str] = None


class ReviewResponse(BaseModel):
    """
    Respuesta completa de una auditoría de Backlog.
    """

    project: ProjectDTO
    quality_score: float
    statistics: StatisticsDTO
    findings: list[FindingDTO]


class ErrorResponse(BaseModel):
    """
    Estructura estándar para mensajes de error.
    """

    detail: str
    error_type: Optional[str] = None
