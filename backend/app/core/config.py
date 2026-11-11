"""Configuración centralizada, leída de variables de entorno o del archivo .env."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parámetros de la API. Cada campo se puede sobrescribir con CLASIFICADOR_<NOMBRE>."""

    model_config = SettingsConfigDict(env_prefix="CLASIFICADOR_", env_file=".env", extra="ignore")

    entorno: str = "desarrollo"
    url_base_datos: str = "sqlite:///./clasificador.db"
    ruta_modelos: Path = Path("../models")
    tamano_maximo_archivo_mb: int = 10
    minimo_terminos: int = 20
    umbral_confianza_dominio: float = 0.60
    umbral_confianza_conjunta: float = 0.40
    origenes_cors: list[str] = ["http://localhost:5173"]


settings = Settings()
