from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_salud_responde_activo():
    respuesta = cliente.get("/api/v1/salud")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "activo"
    assert "version" in datos


def test_documentacion_openapi_disponible():
    assert cliente.get("/openapi.json").status_code == 200
