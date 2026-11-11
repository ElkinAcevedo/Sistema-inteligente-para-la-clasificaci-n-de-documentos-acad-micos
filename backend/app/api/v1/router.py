"""Agrupa los routers de todos los recursos de la versión 1."""

from fastapi import APIRouter

from app.api.v1.endpoints import salud

api_router = APIRouter()
api_router.include_router(salud.router, tags=["salud"])

# Se agregan a medida que se implementen (ver sección 7 del documento de diseño):
# api_router.include_router(categorias.router, tags=["categorías"])
# api_router.include_router(clasificaciones.router, prefix="/clasificaciones")
# api_router.include_router(modelos.router, prefix="/modelos", tags=["modelos"])
