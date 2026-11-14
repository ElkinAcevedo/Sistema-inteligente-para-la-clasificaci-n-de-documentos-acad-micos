"""Carga de los archivos YAML de `ml/configs/`.

Cada configuración de modelo se combina con `base.yaml`, de modo que los parámetros
compartidos (semilla, partición, TF-IDF) se definen una sola vez.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from clasificador_ml.rutas import CONFIGURACIONES

CONFIG_BASE = CONFIGURACIONES / "base.yaml"


def _combinar(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    """Combina dos diccionarios; los valores de `extra` tienen prioridad (fusión profunda)."""
    resultado = dict(base)
    for clave, valor in extra.items():
        if isinstance(valor, dict) and isinstance(resultado.get(clave), dict):
            resultado[clave] = _combinar(resultado[clave], valor)
        else:
            resultado[clave] = valor
    return resultado


def cargar_configuracion(ruta: Path | str | None = None) -> dict[str, Any]:
    """Devuelve `base.yaml` combinado con el archivo indicado (o solo la base si no hay ruta)."""
    base = yaml.safe_load(CONFIG_BASE.read_text(encoding="utf-8")) or {}
    if ruta is None or Path(ruta).resolve() == CONFIG_BASE.resolve():
        return base
    extra = yaml.safe_load(Path(ruta).read_text(encoding="utf-8")) or {}
    return _combinar(base, extra)
