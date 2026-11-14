"""Carga y preparación del dataset WOS-46985 (Fase I).

Flujo:
1. Leer `data/raw/WebOfScience/Meta-data/Data.xlsx`.
2. Limpiar: quitar espacios sobrantes, filas vacías y resúmenes duplicados.
3. Construir etiquetas consistentes con la jerarquía dominio -> área
   (ver `docs/decisiones/0002-etiquetas-wos.md`).
4. Dividir 70/15/15 estratificado por área con semilla fija.
5. Guardar `train/val/test.parquet` y `categorias.json` en `data/processed/`.

Uso:
    python -m clasificador_ml.datos
    python -m clasificador_ml.datos --origen otra/ruta/Data.xlsx --destino otra/carpeta
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split

from clasificador_ml.configuracion import cargar_configuracion
from clasificador_ml.rutas import DATOS_CRUDOS, DATOS_PROCESADOS

ARCHIVO_WOS = DATOS_CRUDOS / "WebOfScience" / "Meta-data" / "Data.xlsx"

COLUMNAS_WOS = ["Y1", "Y2", "Y", "Domain", "area", "keywords", "Abstract"]

# Nombre legible de cada dominio (los códigos son los del dataset, sin espacios).
NOMBRES_DOMINIO: dict[str, tuple[str, str]] = {
    "CS": ("Computer Science", "Ciencias de la computación"),
    "ECE": ("Electrical and Computer Engineering", "Ingeniería eléctrica y electrónica"),
    "Psychology": ("Psychology", "Psicología"),
    "MAE": ("Mechanical and Aerospace Engineering", "Ingeniería mecánica y aeroespacial"),
    "Civil": ("Civil Engineering", "Ingeniería civil"),
    "Medical": ("Medical Sciences", "Ciencias médicas"),
    "biochemistry": ("Biochemistry", "Bioquímica"),
}

# Columnas de las particiones en Parquet.
COLUMNAS_SALIDA = [
    "id_documento",
    "texto",
    "palabras_clave",
    "id_dominio",
    "dominio",
    "id_area",
    "area",
    "y_original",
]


def leer_wos(ruta: Path | str = ARCHIVO_WOS) -> pd.DataFrame:
    """Lee el Excel original de WOS y valida que tenga las columnas esperadas."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Descarga el dataset siguiendo data/README.md."
        )
    df = pd.read_excel(ruta)
    faltantes = set(COLUMNAS_WOS) - set(df.columns)
    if faltantes:
        raise ValueError(f"Al archivo le faltan columnas: {sorted(faltantes)}")
    df = df[COLUMNAS_WOS].copy()
    df.insert(0, "id_documento", range(len(df)))  # fila original, para trazabilidad
    return df


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Quita espacios sobrantes, filas sin resumen o sin etiquetas y resúmenes duplicados."""
    df = df.copy()
    for columna in ["Domain", "area", "keywords", "Abstract"]:
        df[columna] = df[columna].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    df = df.dropna(subset=["Y1", "Y", "Domain", "area", "Abstract"])
    df = df[df["Abstract"].str.len() > 0]
    df["keywords"] = df["keywords"].fillna("")
    # Duplicados por contenido, sin distinguir mayúsculas.
    df = df[~df["Abstract"].str.lower().duplicated(keep="first")]
    return df.reset_index(drop=True)


def construir_etiquetas(
    df: pd.DataFrame, min_documentos_por_area: int = 10
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Asigna `id_dominio`, `id_area` y sus nombres, y devuelve la jerarquía de categorías.

    El id global `Y` del dataset no siempre pertenece a un único dominio (p. ej. *Depression*
    aparece en Medical y en Psychology). Por eso cada área se identifica con el par
    (dominio, Y): así todas las áreas cuelgan de exactamente un dominio. Las áreas con menos de
    `min_documentos_por_area` documentos se descartan por ser ruido de etiquetado.
    """
    df = df.copy()
    df["Y1"] = df["Y1"].astype(int)
    df["Y"] = df["Y"].astype(int)

    # Y1 identifica el dominio; su nombre es el texto de `Domain` (un único valor por Y1).
    codigo_por_y1 = df.groupby("Y1")["Domain"].agg(lambda s: s.mode().iat[0])
    if df.groupby("Y1")["Domain"].nunique().max() > 1:
        raise ValueError("Hay un Y1 asociado a más de un dominio: revisar el dataset.")

    tamanos = df.groupby(["Y1", "Y"]).size()
    validos = tamanos[tamanos >= min_documentos_por_area].index
    df = df[pd.MultiIndex.from_frame(df[["Y1", "Y"]]).isin(validos)].reset_index(drop=True)

    # Ids contiguos: dominios 0..6 tal como vienen; áreas ordenadas por (dominio, Y).
    pares = sorted(validos)
    id_area_por_par = {par: i for i, par in enumerate(pares)}
    df["id_dominio"] = df["Y1"]
    df["dominio"] = df["Y1"].map(codigo_por_y1)
    df["id_area"] = [id_area_por_par[par] for par in zip(df["Y1"], df["Y"], strict=True)]

    # El texto de `area` tiene variantes dentro de un mismo Y: se usa el más frecuente
    # como nombre y el resto queda como alias.
    variantes = df.groupby("id_area")["area"].value_counts()
    nombre_area = {i: variantes[i].index[0] for i in variantes.index.get_level_values(0).unique()}
    df["area"] = df["id_area"].map(nombre_area)
    df["y_original"] = df["Y"]
    df["texto"] = df["Abstract"]
    df["palabras_clave"] = df["keywords"]

    conteo_area = df["id_area"].value_counts()
    dominios = []
    for y1 in sorted(codigo_por_y1.index):
        codigo = codigo_por_y1[y1]
        nombre, nombre_es = NOMBRES_DOMINIO.get(codigo, (codigo, codigo))
        areas = [
            {
                "id": id_area_por_par[(d, y)],
                "nombre": nombre_area[id_area_por_par[(d, y)]],
                "alias": list(variantes[id_area_por_par[(d, y)]].index[1:]),
                "y_original": int(y),
                "documentos": int(conteo_area[id_area_por_par[(d, y)]]),
            }
            for d, y in pares
            if d == y1
        ]
        dominios.append(
            {
                "id": int(y1),
                "codigo": codigo,
                "nombre": nombre,
                "nombre_es": nombre_es,
                "documentos": int(sum(a["documentos"] for a in areas)),
                "areas": areas,
            }
        )

    categorias = {
        "fuente": "Web of Science WOS-46985 (Kowsari et al., 2017)",
        "total_dominios": len(dominios),
        "total_areas": len(pares),
        "dominios": dominios,
    }
    return df[COLUMNAS_SALIDA], categorias


def dividir(
    df: pd.DataFrame,
    proporciones: tuple[float, float, float] = (0.70, 0.15, 0.15),
    semilla: int = 42,
    estratificar_por: str = "id_area",
) -> dict[str, pd.DataFrame]:
    """Divide en entrenamiento, validación y prueba, estratificando por la columna indicada."""
    entrenamiento, validacion, prueba = proporciones
    if abs(entrenamiento + validacion + prueba - 1.0) > 1e-6:
        raise ValueError(f"Las proporciones deben sumar 1, se recibió {proporciones}")

    train, resto = train_test_split(
        df,
        train_size=entrenamiento,
        random_state=semilla,
        stratify=df[estratificar_por],
    )
    val, test = train_test_split(
        resto,
        test_size=prueba / (validacion + prueba),
        random_state=semilla,
        stratify=resto[estratificar_por],
    )
    return {
        "train": train.reset_index(drop=True),
        "val": val.reset_index(drop=True),
        "test": test.reset_index(drop=True),
    }


def guardar(
    particiones: dict[str, pd.DataFrame],
    categorias: dict[str, Any],
    destino: Path | str = DATOS_PROCESADOS,
) -> None:
    """Escribe cada partición en Parquet y la jerarquía (con tamaños) en `categorias.json`."""
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, particion in particiones.items():
        particion.to_parquet(destino / f"{nombre}.parquet", index=False)
    categorias = {
        **categorias,
        "particiones": {nombre: len(p) for nombre, p in particiones.items()},
    }
    (destino / "categorias.json").write_text(
        json.dumps(categorias, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def preparar_dataset(
    origen: Path | str = ARCHIVO_WOS,
    destino: Path | str = DATOS_PROCESADOS,
    config: dict[str, Any] | None = None,
) -> dict[str, pd.DataFrame]:
    """Ejecuta el flujo completo de la Fase I y devuelve las particiones."""
    config = config or cargar_configuracion()
    particion = config["particion"]
    datos = config.get("datos", {})

    crudo = leer_wos(origen)
    limpio = limpiar(crudo)
    etiquetado, categorias = construir_etiquetas(
        limpio, min_documentos_por_area=datos.get("min_documentos_por_area", 10)
    )
    particiones = dividir(
        etiquetado,
        proporciones=(particion["entrenamiento"], particion["validacion"], particion["prueba"]),
        semilla=config["semilla"],
        estratificar_por=particion.get("estratificar_por", "id_area"),
    )
    categorias["limpieza"] = {
        "filas_originales": len(crudo),
        "filas_tras_limpieza": len(limpio),
        "filas_finales": len(etiquetado),
        "descartadas_por_area_pequena": len(limpio) - len(etiquetado),
    }
    guardar(particiones, categorias, destino)
    return particiones


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Prepara el dataset WOS-46985 (Fase I).")
    parser.add_argument("--origen", type=Path, default=ARCHIVO_WOS, help="Ruta a Data.xlsx")
    parser.add_argument("--destino", type=Path, default=DATOS_PROCESADOS)
    parser.add_argument("--config", type=Path, default=None, help="YAML de ml/configs/")
    args = parser.parse_args(argv)

    particiones = preparar_dataset(args.origen, args.destino, cargar_configuracion(args.config))
    resumen = ", ".join(f"{nombre}={len(p)}" for nombre, p in particiones.items())
    print(f"Particiones guardadas en {args.destino}: {resumen}")


if __name__ == "__main__":
    main()
