"""
FastAPI Application Factory.
"""

from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.presentation.api.routes import router

load_dotenv()


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    app = FastAPI(
        title="Backlog Review Agent API",
        description="API REST para auditoría y evaluación de calidad de Backlogs en Jira.",
        version="1.0.0",
    )

    # -------------------------------------------------------------
    # Configuración de CORS segura y selectiva
    # -------------------------------------------------------------
    cors_env = os.getenv("CORS_ORIGINS")
    if cors_env:
        origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    else:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------
    # Routers
    # -------------------------------------------------------------
    app.include_router(router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "service": "backlog-review-agent"}

    return app


app = create_app()
