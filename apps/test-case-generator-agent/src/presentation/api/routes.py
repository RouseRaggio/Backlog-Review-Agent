"""
API Routes for Test Case Generator Agent.
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.analyze_user_story import AnalyzeUserStoryUseCase
from src.application.use_cases.generate_test_cases import GenerateTestCasesUseCase
from src.bootstrap.dependency_injection import (
    build_analyze_use_case,
    build_generate_use_case,
)
from src.domain.services.jira_gateway import (
    JiraConfigError,
    JiraConnectionError,
    JiraError,
    JiraPermissionError,
    JiraTimeoutError,
    UserStoryNotFoundError,
)
from src.presentation.api.mappers import (
    map_analysis_to_response,
    map_request_to_domain,
    map_result_to_response,
)
from src.presentation.api.schemas import (
    AnalyzeUserStoryRequest,
    AnalyzeUserStoryResponse,
    ErrorResponse,
    GenerateTestCasesRequest,
    GenerateTestCasesResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Test Cases"])


def get_generate_use_case() -> GenerateTestCasesUseCase:
    """Proveedor de dependencias para GenerateTestCasesUseCase."""
    return build_generate_use_case()


def get_analyze_use_case() -> AnalyzeUserStoryUseCase:
    """Proveedor de dependencias para AnalyzeUserStoryUseCase."""
    return build_analyze_use_case()


@router.post(
    "/test-cases/analyze",
    response_model=AnalyzeUserStoryResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Error de configuración o parámetros"},
        403: {"model": ErrorResponse, "description": "Permisos insuficientes en Jira"},
        404: {"model": ErrorResponse, "description": "Historia no encontrada en Jira"},
        502: {"model": ErrorResponse, "description": "Error de conexión o timeout con Jira"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
    summary="Analizar Historia de Usuario desde Jira",
    description="Consulta Jira para obtener la Historia de Usuario y sus Criterios de Aceptación, diagnosticando la suficiencia antes de generar casos de prueba.",
)
def analyze_user_story(
    request: AnalyzeUserStoryRequest,
    use_case: Annotated[AnalyzeUserStoryUseCase, Depends(get_analyze_use_case)],
) -> AnalyzeUserStoryResponse:
    """
    Analiza una Historia de Usuario desde Jira.
    """
    try:
        result = use_case.execute(
            project_key=request.project_key,
            issue_key=request.issue_key,
        )
        return map_analysis_to_response(result)

    except UserStoryNotFoundError as e:
        logger.warning(f"Issue no encontrada en Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except JiraPermissionError as e:
        logger.warning(f"Error de permisos en Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    except (JiraConnectionError, JiraTimeoutError) as e:
        logger.error(f"Fallo de conexión o timeout con Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )

    except JiraConfigError as e:
        logger.warning(f"Configuración de Jira incompleta: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except ValueError as e:
        logger.warning(f"Validación fallida: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        logger.exception(f"Error inesperado al analizar historia: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al analizar la Historia de Usuario.",
        )


@router.post(
    "/test-cases/generate",
    response_model=GenerateTestCasesResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Entrada inválida o error de configuración"},
        403: {"model": ErrorResponse, "description": "Permisos insuficientes en Jira"},
        404: {"model": ErrorResponse, "description": "Historia no encontrada en Jira"},
        422: {"description": "Error de validación en la solicitud"},
        502: {"model": ErrorResponse, "description": "Error de comunicación con Jira"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
    summary="Generar casos de prueba a partir de Historia y Criterios",
    description="Genera casos de prueba estructurados y trazables consultando Jira automáticamente o utilizando el payload manual provisto.",
)
def generate_test_cases(
    request: GenerateTestCasesRequest,
    use_case: Annotated[GenerateTestCasesUseCase, Depends(get_generate_use_case)],
) -> GenerateTestCasesResponse:
    """
    Genera casos de prueba estructurados.
    """
    try:
        story, criteria, options = map_request_to_domain(request)
        result = use_case.execute(
            story=story,
            criteria=criteria,
            options=options,
            project_key=request.project_key,
            issue_key=request.issue_key,
        )
        return map_result_to_response(result)

    except UserStoryNotFoundError as e:
        logger.warning(f"Issue no encontrada en Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except JiraPermissionError as e:
        logger.warning(f"Error de permisos en Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    except (JiraConnectionError, JiraTimeoutError) as e:
        logger.error(f"Fallo de conexión o timeout con Jira: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )

    except (JiraConfigError, ValueError) as e:
        logger.warning(f"Error de validación en generación: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        logger.exception(f"Error inesperado al generar casos de prueba: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al generar los casos de prueba.",
        )
