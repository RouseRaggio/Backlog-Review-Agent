"""
Presentation API Schemas / DTOs for Test Case Generator Agent.
"""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class CriterionDTO(BaseModel):
    """
    DTO para un Criterio de Aceptación.
    """

    id: str = Field(..., description="Identificador del criterio (ej. AC-001)", examples=["AC-001"])
    description: str = Field(..., description="Texto descriptivo del criterio", examples=["El correo electrónico debe ser único."])


class GenerationOptionsDTO(BaseModel):
    """
    DTO para opciones de configuración de generación.
    """

    include_positive: bool = Field(default=True, description="Incluir casos de prueba positivos")
    include_negative: bool = Field(default=True, description="Incluir casos de prueba negativos")
    include_validation: bool = Field(default=True, description="Incluir casos de validación")
    include_boundary: bool = Field(default=True, description="Incluir casos límite cuando existan umbrales")
    detail_level: str = Field(default="standard", description="Nivel de detalle: basic, standard, detailed")
    min_priority: str = Field(default="LOW", description="Prioridad mínima a incluir: LOW, MEDIUM, HIGH, CRITICAL")


class AnalyzeUserStoryRequest(BaseModel):
    """
    Request DTO para analizar una Historia de Usuario desde Jira.
    """

    project_key: str = Field(..., description="Clave del proyecto Jira (ej. GES)", examples=["GES"])
    issue_key: str = Field(..., description="Clave de la Historia/Issue en Jira (ej. GES-40)", examples=["GES-40"])

    @field_validator("project_key")
    @classmethod
    def validate_project_key(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("project_key no puede estar vacío.")
        return cleaned

    @field_validator("issue_key")
    @classmethod
    def validate_issue_key(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("issue_key no puede estar vacío.")
        return cleaned


class UserStoryPreviewDTO(BaseModel):
    """
    DTO para la previsualización de una Historia de Usuario.
    """

    title: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    benefit: Optional[str] = None
    raw_text: str


class AnalyzeUserStoryResponse(BaseModel):
    """
    Response DTO del análisis previo de una Historia de Usuario.
    """

    project: ProjectInfoDTO
    user_story: UserStoryPreviewDTO
    acceptance_criteria: list[CriterionDTO] = Field(default_factory=list)
    qa_tests: list[str] = Field(default_factory=list)
    source: str = "jira"
    sufficient_information: bool = True
    confidence: str = "HIGH"
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)



class GenerateTestCasesRequest(BaseModel):
    """
    Request DTO para la generación de casos de prueba.
    Soporta consulta automática a Jira o fallback manual.
    """

    project_key: str = Field(..., description="Clave del proyecto (ej. GES, CAP)", examples=["GES"])
    issue_key: str = Field(..., description="Clave de la Historia/Issue (ej. GES-123)", examples=["GES-123"])
    user_story: Optional[str] = Field(default=None, description="Texto opcional de la Historia (si es manual)")
    acceptance_criteria: list[CriterionDTO] = Field(default_factory=list, description="Lista opcional de criterios de aceptación")
    options: GenerationOptionsDTO = Field(default_factory=GenerationOptionsDTO, description="Opciones de generación")

    @field_validator("project_key")
    @classmethod
    def validate_project_key(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("project_key no puede estar vacío.")
        return cleaned

    @field_validator("issue_key")
    @classmethod
    def validate_issue_key(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("issue_key no puede estar vacío.")
        return cleaned


class TestCaseDTO(BaseModel):
    """
    DTO para un Caso de Prueba generado.
    """

    id: str
    title: str
    description: str
    type: str
    category: str
    priority: str
    preconditions: list[str] = Field(default_factory=list)
    required_data: dict[str, str] = Field(default_factory=dict)
    steps: list[str] = Field(default_factory=list)
    expected_result: str
    requirement_reference: str
    acceptance_criteria_reference: Optional[str] = None
    confidence: str
    status: str


class ProjectInfoDTO(BaseModel):
    """
    DTO para información del proyecto/issue.
    """

    key: str
    issue_key: str


class SummaryMetricsDTO(BaseModel):
    """
    DTO para métricas consolidadas de generación.
    """

    total_cases: int
    positive_count: int
    negative_count: int
    validation_count: int
    boundary_count: int
    traceability_rate: float
    overall_confidence: str


class GenerateTestCasesResponse(BaseModel):
    """
    Response DTO completa de la generación de casos de prueba.
    """

    project: ProjectInfoDTO
    summary: SummaryMetricsDTO
    warnings: list[str] = Field(default_factory=list)
    test_cases: list[TestCaseDTO] = Field(default_factory=list)
    traceability: dict[str, list[str]] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """
    DTO estándar para respuestas de error.
    """

    detail: str
    error_type: Optional[str] = None
