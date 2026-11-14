import json

import pandas as pd
import pytest

from clasificador_ml.configuracion import cargar_configuracion
from clasificador_ml.datos import (
    COLUMNAS_SALIDA,
    construir_etiquetas,
    dividir,
    leer_wos,
    limpiar,
    preparar_dataset,
)


def _fila(y1, y, dominio, area, n):
    return {
        "Y1": y1,
        "Y2": 0,
        "Y": y,
        "Domain": f"{dominio} ",
        "area": f" {area}  ",
        "keywords": "kw1; kw2",
        "Abstract": f" Resumen {n} sobre {area} ",
    }


@pytest.fixture
def wos_sintetico() -> pd.DataFrame:
    """Mini WOS que reproduce los problemas del dataset real."""
    filas = []
    n = 0
    plan = [
        (0, 0, "CS", "Computer vision", 30),
        (0, 1, "CS", "Machine learning", 30),
        # Mismo Y en dos dominios (como Depression en Medical y Psychology).
        (1, 2, "Psychology", "Depression", 30),
        (2, 2, "Medical", "Depression", 30),
        (2, 3, "Medical", "Cancer", 28),
        # Variante de nombre dentro del mismo Y.
        (2, 3, "Medical", "Oncology", 2),
        # Área diminuta: debe descartarse.
        (3, 4, "Civil", "Bamboo", 2),
        (3, 5, "Civil", "Geotextile", 30),
    ]
    for y1, y, dominio, area, cantidad in plan:
        for _ in range(cantidad):
            filas.append(_fila(y1, y, dominio, area, n))
            n += 1
    df = pd.DataFrame(filas)
    df.insert(0, "id_documento", range(len(df)))
    return df


def test_limpiar_quita_espacios_y_duplicados(wos_sintetico):
    sucio = pd.concat([wos_sintetico, wos_sintetico.iloc[[0]]], ignore_index=True)
    sucio.loc[len(sucio) - 1, "Abstract"] = sucio.loc[0, "Abstract"].upper()
    sucio = pd.concat(
        [sucio, pd.DataFrame([{**sucio.iloc[1].to_dict(), "Abstract": "   "}])],
        ignore_index=True,
    )

    limpio = limpiar(sucio)

    assert len(limpio) == len(wos_sintetico)
    assert limpio["Domain"].iloc[0] == "CS"
    assert limpio["area"].iloc[0] == "Computer vision"
    assert not limpio["Abstract"].str.startswith(" ").any()


def test_etiquetas_respetan_la_jerarquia(wos_sintetico):
    df, categorias = construir_etiquetas(limpiar(wos_sintetico), min_documentos_por_area=10)

    assert list(df.columns) == COLUMNAS_SALIDA
    # Cada área pertenece a un único dominio.
    assert df.groupby("id_area")["id_dominio"].nunique().max() == 1
    # Depression queda como dos áreas distintas, una por dominio.
    depresion = df[df["area"] == "Depression"]
    assert depresion["id_area"].nunique() == 2
    # Las áreas son contiguas desde 0.
    assert sorted(df["id_area"].unique()) == list(range(df["id_area"].nunique()))
    assert categorias["total_areas"] == 6
    assert categorias["total_dominios"] == 4


def test_area_pequena_se_descarta(wos_sintetico):
    df, categorias = construir_etiquetas(limpiar(wos_sintetico), min_documentos_por_area=10)

    assert "Bamboo" not in set(df["area"])
    civil = next(d for d in categorias["dominios"] if d["codigo"] == "Civil")
    assert [a["nombre"] for a in civil["areas"]] == ["Geotextile"]


def test_variantes_de_nombre_quedan_como_alias(wos_sintetico):
    df, categorias = construir_etiquetas(limpiar(wos_sintetico))

    assert "Oncology" not in set(df["area"])
    medical = next(d for d in categorias["dominios"] if d["codigo"] == "Medical")
    cancer = next(a for a in medical["areas"] if a["nombre"] == "Cancer")
    assert cancer["alias"] == ["Oncology"]
    assert cancer["documentos"] == 30
    assert medical["nombre_es"] == "Ciencias médicas"


def test_dividir_es_estratificado_y_sin_fugas(wos_sintetico):
    df, _ = construir_etiquetas(limpiar(wos_sintetico))

    particiones = dividir(df, proporciones=(0.70, 0.15, 0.15), semilla=42)

    ids = [set(p["id_documento"]) for p in particiones.values()]
    assert ids[0].isdisjoint(ids[1]) and ids[0].isdisjoint(ids[2]) and ids[1].isdisjoint(ids[2])
    assert sum(len(p) for p in particiones.values()) == len(df)
    for particion in particiones.values():
        assert particion["id_area"].nunique() == df["id_area"].nunique()
    assert abs(len(particiones["train"]) / len(df) - 0.70) < 0.02


def test_dividir_es_reproducible(wos_sintetico):
    df, _ = construir_etiquetas(limpiar(wos_sintetico))

    a = dividir(df, semilla=42)["test"]["id_documento"].tolist()
    b = dividir(df, semilla=42)["test"]["id_documento"].tolist()

    assert a == b


def test_dividir_rechaza_proporciones_invalidas(wos_sintetico):
    df, _ = construir_etiquetas(limpiar(wos_sintetico))

    with pytest.raises(ValueError):
        dividir(df, proporciones=(0.8, 0.15, 0.15))


def test_leer_wos_avisa_si_falta_el_archivo(tmp_path):
    with pytest.raises(FileNotFoundError, match="data/README.md"):
        leer_wos(tmp_path / "no_existe.xlsx")


def test_flujo_completo_escribe_particiones(tmp_path, wos_sintetico):
    origen = tmp_path / "Data.xlsx"
    wos_sintetico.drop(columns="id_documento").to_excel(origen, index=False)
    destino = tmp_path / "processed"

    particiones = preparar_dataset(origen, destino, cargar_configuracion())

    for nombre in ("train", "val", "test"):
        guardado = pd.read_parquet(destino / f"{nombre}.parquet")
        assert len(guardado) == len(particiones[nombre])
    categorias = json.loads((destino / "categorias.json").read_text(encoding="utf-8"))
    assert categorias["limpieza"]["descartadas_por_area_pequena"] == 2
    assert sum(categorias["particiones"].values()) == categorias["limpieza"]["filas_finales"]


def test_configuracion_combina_con_base(tmp_path):
    extra = tmp_path / "modelo.yaml"
    extra.write_text("modelo: prueba\nparticion:\n  prueba: 0.2\n", encoding="utf-8")

    config = cargar_configuracion(extra)

    assert config["modelo"] == "prueba"
    assert config["particion"]["prueba"] == 0.2
    assert config["particion"]["entrenamiento"] == 0.70
    assert config["semilla"] == 42
