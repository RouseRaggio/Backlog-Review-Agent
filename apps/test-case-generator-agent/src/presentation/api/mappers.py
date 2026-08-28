"""
Presentation Mappers for Test Case Generator Agent.
"""

from __future__ import annotations

from typing import Optional
from src.application.use_cases.analyze_user_story import AnalysisResult
from src.domain.entities import (
    AcceptanceCriterion,
    GenerationOptions,
    GenerationResult,
    TestCase,
    UserStory,
)
from src.domain.enums import Priority
from src.presentation.api.schemas import (
    AnalyzeUserStoryResponse,
    CriterionDTO,
    GenerateTestCasesRequest,
    GenerateTestCasesResponse,
    ProjectInfoDTO,
    SummaryMetricsDTO,
    TestCaseDTO,
    UserStoryPreviewDTO,
)


def map_request_to_domain(
    request: GenerateTestCasesRequest,
) -> tuple[Optional[UserStory], Optional[list[AcceptanceCriterion]], GenerationOptions]:
    """
    Convierte el DTO de entrada a entidades y opciones de dominio.
    Si user_story no se proporciona, retorna story=None para que se consulte Jira.
    """
    story = None
    if request.user_story and request.user_story.strip():
        story = UserStory(
            project_key=request.project_key,
            issue_key=request.issue_key,
            raw_text=request.user_story,
        )

    criteria = None
    if request.acceptance_criteria:
        criteria = [
            AcceptanceCriterion(
                id=c.id,
                description=c.description,
            )
            for c in request.acceptance_criteria
        ]

    try:
        min_prio = Priority(request.options.min_priority.upper())
    except ValueError:
        min_prio = Priority.LOW

    options = GenerationOptions(
        include_positive=request.options.include_positive,
        include_negative=request.options.include_negative,
        include_validation=request.options.include_validation,
        include_boundary=request.options.include_boundary,
        detail_level=request.options.detail_level,
        min_priority=min_prio,
    )

    return story, criteria, options


def map_analysis_to_response(result: AnalysisResult) -> AnalyzeUserStoryResponse:
    """
    Convierte el AnalysisResult a AnalyzeUserStoryResponse DTO.
    """
    project = ProjectInfoDTO(
        key=result.project_key,
        issue_key=result.issue_key,
    )

    user_story_dto = UserStoryPreviewDTO(
        title=result.story.title,
        role=result.story.role,
        goal=result.story.goal,
        benefit=result.story.benefit,
        raw_text=result.story.raw_text,
    )

    criteria_dtos = [
        CriterionDTO(id=c.id, description=c.description)
        for c in result.criteria
    ]

    return AnalyzeUserStoryResponse(
        project=project,
        user_story=user_story_dto,
        acceptance_criteria=criteria_dtos,
        qa_tests=result.qa_tests,
        source=result.source,
        sufficient_information=result.sufficient_information,
        confidence=result.confidence.value,
        warnings=result.warnings,
        metadata=result.metadata,
    )



def map_test_case_to_dto(tc: TestCase) -> TestCaseDTO:
    """
    Convierte un TestCase de dominio a TestCaseDTO.
    """
    return TestCaseDTO(
        id=tc.id,
        title=tc.title,
        description=tc.description,
        type=tc.type.value,
        category=tc.category.value,
        priority=tc.priority.value,
        preconditions=tc.preconditions,
        required_data=tc.required_data,
        steps=tc.steps,
        expected_result=tc.expected_result,
        requirement_reference=tc.requirement_reference,
        acceptance_criteria_reference=tc.acceptance_criteria_reference,
        confidence=tc.confidence.value,
        status=tc.status.value,
    )


def map_result_to_response(result: GenerationResult) -> GenerateTestCasesResponse:
    """
    Convierte un GenerationResult de dominio a GenerateTestCasesResponse DTO.
    """
    summary = SummaryMetricsDTO(
        total_cases=result.total_cases,
        positive_count=result.positive_count,
        negative_count=result.negative_count,
        validation_count=result.validation_count,
        boundary_count=result.boundary_count,
        traceability_rate=result.traceability_rate,
        overall_confidence=result.overall_confidence.value,
    )

    project = ProjectInfoDTO(
        key=result.project_key,
        issue_key=result.issue_key,
    )

    test_case_dtos = [map_test_case_to_dto(tc) for tc in result.test_cases]

    return GenerateTestCasesResponse(
        project=project,
        summary=summary,
        warnings=result.warnings,
        test_cases=test_case_dtos,
        traceability=result.traceability_map,
    )
