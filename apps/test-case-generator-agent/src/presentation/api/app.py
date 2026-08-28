"""
FastAPI Application Factory for Test Case Generator Agent.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.routes import router

load_dotenv()


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI para el Test Case Generator Agent.
    """
    app = FastAPI(
        title="Test Case Generator Agent API",
        description="API REST para generación automática, trazable y estructurada de casos de prueba a partir de Historias de Usuario.",
        version="1.0.0",
    )

    # Configuración selectiva de CORS
    cors_env = os.getenv("CORS_ORIGINS")
    if cors_env:
        origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    else:
        origins = [
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "service": "test-case-generator-agent"}

    return app


app = create_app()
