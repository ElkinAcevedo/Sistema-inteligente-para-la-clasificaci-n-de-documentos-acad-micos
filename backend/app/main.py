"""Punto de entrada de la API.

Ejecutar en desarrollo:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    """Construye la aplicación FastAPI con su configuración y rutas."""
    aplicacion = FastAPI(
        title="Clasificador de Documentos Académicos",
        description="Clasifica documentos académicos por dominio y área temática (WOS-46985).",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origenes_cors,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    aplicacion.include_router(api_router, prefix="/api/v1")
    return aplicacion


app = create_app()
