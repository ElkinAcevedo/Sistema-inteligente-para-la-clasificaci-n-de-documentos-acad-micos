from pydantic import BaseModel


class RespuestaSalud(BaseModel):
    estado: str
    version: str
    modelo_activo: str | None
