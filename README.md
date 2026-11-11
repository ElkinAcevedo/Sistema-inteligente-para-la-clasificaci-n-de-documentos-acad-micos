<div align="center">

# Clasificador de Documentos Académicos

**Aplicación web que clasifica documentos académicos por dominio y área temática usando Procesamiento de Lenguaje Natural y aprendizaje automático.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Estado](https://img.shields.io/badge/estado-en%20desarrollo-orange)

Proyecto Integrador · Universidad de Pamplona · 2026

</div>

---

## Tabla de contenido

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Stack tecnológico](#stack-tecnológico)
- [Inicio rápido](#inicio-rápido)
- [Dataset](#dataset)
- [Hoja de ruta](#hoja-de-ruta)
- [Cómo contribuir](#cómo-contribuir)
- [Equipo](#equipo)

## Descripción

Clasificar documentos académicos a mano es lento cuando el volumen crece. Este sistema recibe un documento (PDF, DOCX o TXT), extrae su resumen y predice en dos niveles:

1. **Dominio académico** (7 clases), por ejemplo *Computer Science* o *Medical*.
2. **Área temática** dentro de ese dominio (134 áreas en total), por ejemplo *Computer vision*.

Los modelos se entrenan con el dataset **Web of Science WOS-46985** (Kowsari et al., 2017), que contiene 46.985 resúmenes en inglés etiquetados jerárquicamente.

## Características

- Carga de documentos PDF, DOCX y TXT, o texto pegado directamente.
- Detección automática del resumen (*Abstract*) y del idioma.
- Clasificación jerárquica dominio → área, con nivel de confianza.
- Las 3 alternativas más probables y los términos que más influyeron en la predicción.
- Aviso de **revisión humana** cuando la confianza es baja.
- Historial de clasificaciones y corrección por parte del usuario.
- Panel de métricas con la comparación de 3 modelos: Naive Bayes, SVM lineal y DistilBERT.
- API REST documentada automáticamente con OpenAPI/Swagger.

## Arquitectura

```mermaid
flowchart TB
    U([Usuario]) --> W[Dashboard web<br/>React + TypeScript]
    W -- HTTP / JSON<br/>/api/v1 --> R

    subgraph API [API REST · FastAPI]
        R[Rutas REST] --> E[Extracción<br/>PDF · DOCX · TXT]
        R --> C[Clasificación<br/>TF-IDF · dominio → área]
        R --> P[Persistencia<br/>SQLAlchemy]
        E --> C
    end

    C --> M[(Modelos .joblib)]
    P --> D[(SQLite)]

    subgraph OFF [Fuera de línea]
        DS[(WOS-46985)] --> T[Entrenamiento<br/>notebooks + scripts]
    end
    T -. publica el modelo .-> M
```

La API carga el modelo activo una sola vez al iniciar y **nunca entrena durante una consulta**. El preprocesamiento vive en el paquete compartido `clasificador_ml`, que usan tanto el entrenamiento como la API, para que el texto se procese igual en ambos lados.

## Estructura del repositorio

```text
clasificador-academico/
├── backend/                 # API REST (FastAPI)
│   ├── app/
│   │   ├── api/v1/          # rutas y endpoints
│   │   ├── core/            # configuración
│   │   ├── schemas/         # contratos JSON (Pydantic)
│   │   ├── extraccion/      # texto de PDF/DOCX/TXT, resumen, idioma
│   │   ├── clasificacion/   # carga del modelo y predicción jerárquica
│   │   └── db/              # modelos y acceso a la base de datos
│   └── tests/
├── ml/                      # paquete clasificador_ml: datos, PLN, entrenamiento, evaluación
│   ├── src/clasificador_ml/
│   ├── configs/             # hiperparámetros por modelo (YAML)
│   └── tests/
├── frontend/                # dashboard web (React + TypeScript + Vite)
├── notebooks/               # análisis exploratorio y comparación de modelos
├── data/                    # dataset crudo y procesado (no se versiona)
├── models/                  # modelos entrenados .joblib (no se versionan)
├── tests/e2e/               # pruebas de extremo a extremo (Playwright)
├── docs/                    # documentación y registro de decisiones
└── scripts/                 # utilidades (descarga de datos, etc.)
```

Cada carpeta principal tiene su propio `README.md` con los detalles.

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Backend y ML | Python 3.11, FastAPI, Uvicorn, Pydantic |
| PLN y modelos | scikit-learn, spaCy, NLTK, Hugging Face Transformers, PyTorch |
| Extracción | PyMuPDF, python-docx, langdetect |
| Datos | SQLite + SQLAlchemy, pandas, Parquet |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, Recharts |
| Pruebas | pytest, httpx, Vitest, Playwright |
| Despliegue | Docker, Docker Compose, GitHub Actions |

## Inicio rápido

> El proyecto está en su fase inicial. Por ahora la API solo expone `GET /api/v1/salud`.

### Requisitos

- Python 3.11 o 3.12
- Node.js 20 o superior (para el frontend)
- Git

### Instalación del backend y el paquete ML

```bash
git clone https://github.com/<usuario>/clasificador-academico.git
cd clasificador-academico

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -e "ml[dev]" -e "backend[dev]"
```

### Ejecutar la API

```bash
cd backend
cp .env.example .env
uvicorn app.main:app --reload
```

Abre <http://localhost:8000/docs> para ver la documentación interactiva.

### Ejecutar las pruebas

```bash
pytest ml/tests
cd backend && pytest
```

## Dataset

El dataset **no se incluye en el repositorio** por su tamaño. Las instrucciones para descargarlo y ubicarlo están en [`data/README.md`](data/README.md).

## Hoja de ruta

| Fase | Semanas | Estado |
| --- | --- | --- |
| I. Revisión y preparación de los datos | 1–2 | ⏳ Pendiente |
| II. Extracción y procesamiento del texto | 2–4 | ⏳ Pendiente |
| III. Entrenamiento y evaluación de modelos | 4–7 | ⏳ Pendiente |
| IV. Desarrollo e integración de la aplicación | 6–9 | 🚧 Estructura base lista |
| V. Pruebas, ajustes y documentación | 10–12 | ⏳ Pendiente |

## Cómo contribuir

Lee la [guía de contribución](CONTRIBUTING.md): flujo de ramas, convención de commits y cómo abrir un *pull request*.

## Equipo

| Integrante | Rol |
| --- | --- |
| Elkin David Acevedo Florez | Por definir |
| Diego Rodriges | Por definir |
| Wilson Alexander Nova | Por definir |

## Referencias

- Kowsari, K., Brown, D. E., Heidarysafa, M., Meimandi, K. J., Gerber, M. S., & Barnes, L. E. (2017). *HDLTex: Hierarchical Deep Learning for Text Classification*. IEEE ICMLA.
