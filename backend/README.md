# Backend · API REST

API construida con **FastAPI** que recibe documentos, extrae su texto, los clasifica con el modelo activo y guarda el historial.

## Estructura

```text
backend/
├── app/
│   ├── main.py              # crea la aplicación FastAPI
│   ├── core/config.py       # configuración (variables CLASIFICADOR_*)
│   ├── api/v1/
│   │   ├── router.py        # agrupa los routers
│   │   └── endpoints/       # un archivo por recurso
│   ├── schemas/             # modelos Pydantic de entrada y salida
│   ├── extraccion/          # PDF, DOCX, TXT → texto; resumen; idioma
│   ├── clasificacion/       # carga del modelo y predicción jerárquica
│   └── db/                  # SQLAlchemy: tablas y repositorios
└── tests/
```

## Ejecutar

Desde la raíz del repositorio, con el entorno virtual activado:

```bash
pip install -e "ml[dev]" -e "backend[dev]"
cd backend
cp .env.example .env
uvicorn app.main:app --reload
```

- Documentación interactiva: <http://localhost:8000/docs>
- Estado: <http://localhost:8000/api/v1/salud>

## Configuración

Todas las variables usan el prefijo `CLASIFICADOR_` y se leen del archivo `.env` (ver `.env.example`).

| Variable | Valor por defecto | Descripción |
| --- | --- | --- |
| `CLASIFICADOR_URL_BASE_DATOS` | `sqlite:///./clasificador.db` | Conexión a la base de datos. |
| `CLASIFICADOR_RUTA_MODELOS` | `../models` | Carpeta con los modelos entrenados. |
| `CLASIFICADOR_TAMANO_MAXIMO_ARCHIVO_MB` | `10` | Tamaño máximo de archivo aceptado. |
| `CLASIFICADOR_UMBRAL_CONFIANZA_DOMINIO` | `0.60` | Por debajo de este valor se marca «requiere revisión». |
| `CLASIFICADOR_UMBRAL_CONFIANZA_CONJUNTA` | `0.40` | Umbral de la confianza dominio × área. |
| `CLASIFICADOR_ORIGENES_CORS` | `["http://localhost:5173"]` | Orígenes permitidos (frontend). |

## Endpoints

| Método | Ruta | Estado |
| --- | --- | --- |
| GET | `/api/v1/salud` | ✅ Implementado |
| GET | `/api/v1/categorias` | ⏳ Pendiente |
| POST | `/api/v1/clasificaciones/archivo` | ⏳ Pendiente |
| POST | `/api/v1/clasificaciones/texto` | ⏳ Pendiente |
| GET | `/api/v1/clasificaciones` | ⏳ Pendiente |
| GET | `/api/v1/clasificaciones/{id}` | ⏳ Pendiente |
| POST | `/api/v1/clasificaciones/{id}/correccion` | ⏳ Pendiente |
| GET | `/api/v1/modelos` | ⏳ Pendiente |
| GET | `/api/v1/modelos/{id}/metricas` | ⏳ Pendiente |

Los contratos completos están en la sección 7 del documento de diseño.

## Pruebas

```bash
cd backend
pytest --cov=app
```
