"""Rutas estándar del repositorio, calculadas desde la ubicación de este archivo."""

from pathlib import Path

RAIZ_REPOSITORIO = Path(__file__).resolve().parents[3]
DATOS = RAIZ_REPOSITORIO / "data"
DATOS_CRUDOS = DATOS / "raw"
DATOS_PROCESADOS = DATOS / "processed"
MODELOS = RAIZ_REPOSITORIO / "models"
CONFIGURACIONES = RAIZ_REPOSITORIO / "ml" / "configs"
