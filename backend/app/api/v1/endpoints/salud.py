"""GET /api/v1/salud: comprueba que la API está activa."""

from fastapi import APIRouter

from app import __version__
from app.schemas.salud import RespuestaSalud

router = APIRouter()


@router.get("/salud", response_model=RespuestaSalud, summary="Estado de la API")
def obtener_salud() -> RespuestaSalud:
    # TODO(Fase IV): reportar el modelo activo cuando exista el registro de modelos.
    return RespuestaSalud(estado="activo", version=__version__, modelo_activo=None)
