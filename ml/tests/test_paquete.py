from clasificador_ml import __version__
from clasificador_ml.rutas import MODELOS, RAIZ_REPOSITORIO


def test_version_definida():
    assert __version__


def test_rutas_apuntan_al_repositorio():
    assert (RAIZ_REPOSITORIO / "ml").is_dir()
    assert MODELOS.parent == RAIZ_REPOSITORIO
