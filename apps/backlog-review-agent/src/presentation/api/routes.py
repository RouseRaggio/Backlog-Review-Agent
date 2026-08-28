"""
API Routes for Backlog Review Agent.
"""

from __future__ import annotations

import logging
from pathlib import Path
import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
import requests

from src.application.use_cases.audit_backlog import AuditBacklogUseCase
from src.bootstrap.dependency_injection import build_application
from src.presentation.api.mappers import map_audit_report_to_response
from src.presentation.api.schemas import ErrorResponse, ReviewRequest, ReviewResponse
from src.presentation.html.html_report_generator import HtmlReportGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Reviews"])


def get_audit_use_case() -> AuditBacklogUseCase:
    """
    Proveedor de dependencias para el caso de uso AuditBacklogUseCase.
    Reutiliza el Composition Root (build_application).
    """
    return build_application()


@router.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Parámetros inválidos o configuración faltante"},
        422: {"description": "Error de validación en la solicitud"},
        502: {"model": ErrorResponse, "description": "Error al comunicarse con el servicio de Jira"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
    summary="Ejecutar auditoría de Backlog",
    description="Obtiene las historias de un proyecto en Jira, ejecuta el motor de reglas, genera el reporte HTML y calcula el Backlog Quality Score.",
)
def create_review(
    request: ReviewRequest,
    use_case: Annotated[AuditBacklogUseCase, Depends(get_audit_use_case)],
) -> ReviewResponse:
    """
    Inicia una auditoría de calidad sobre un proyecto Jira.
    """
    try:
        report = use_case.execute(
            project_key=request.project_key,
            max_results=request.max_results,
        )

        # Generar reporte HTML automáticamente para habilitar su descarga inmediata
        try:
            generator = HtmlReportGenerator()
            generator.generate(report)
        except Exception as gen_err:
            logger.warning(f"No se pudo generar el reporte HTML estático: {gen_err}")

        return map_audit_report_to_response(report)

    except ValueError as e:
        logger.warning(f"Error de validación o configuración: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de comunicación con Jira: {e}")
        error_msg = "Error al comunicarse con el servicio Jira."
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 401:
                error_msg = "Credenciales de Jira inválidas o no autorizadas."
            elif e.response.status_code == 404:
                error_msg = f"El proyecto '{request.project_key}' no fue encontrado en Jira."
            else:
                error_msg = f"Error en Jira (HTTP {e.response.status_code}): {e.response.text[:150]}"
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=error_msg,
        )

    except Exception as e:
        logger.exception(f"Error inesperado al auditar backlog: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al procesar la auditoría.",
        )


@router.get(
    "/reviews/{project_key}/report",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"text/html": {}},
            "description": "Reporte HTML generado para el proyecto",
        },
        400: {"model": ErrorResponse, "description": "Clave de proyecto inválida o intento de acceso no permitido"},
        404: {"model": ErrorResponse, "description": "Reporte no encontrado para el proyecto especificado"},
    },
    summary="Descargar reporte HTML de auditoría",
    description="Descarga el reporte HTML más reciente generado para el proyecto Jira indicado.",
)
def download_review_report(project_key: str) -> FileResponse:
    """
    Descarga el archivo HTML de auditoría para un proyecto.
    """
    # Validación estricta para prevenir path traversal
    if not re.match(r"^[A-Za-z0-9_-]+$", project_key):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Clave de proyecto inválida. Solo se permiten caracteres alfanuméricos, guiones y guiones bajos.",
        )

    cleaned_key = project_key.strip().upper()
    base_dir = Path("reports/latest").resolve()
    file_path = (base_dir / f"{cleaned_key}_AUDIT.html").resolve()

    # Verificación de confinamiento en el directorio de reportes
    if not file_path.is_relative_to(base_dir):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ruta de acceso no permitida.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte no encontrado para el proyecto '{cleaned_key}'. Ejecuta primero una revisión.",
        )

    return FileResponse(
        path=file_path,
        media_type="text/html",
        filename=f"{cleaned_key}_AUDIT.html",
    )
