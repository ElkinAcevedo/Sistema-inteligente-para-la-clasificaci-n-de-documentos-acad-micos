# Datos

Esta carpeta **no se sube a GitHub** (solo los `.gitkeep` y este archivo). Cada integrante descarga el dataset en su equipo.

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `raw/` | Dataset original tal como se descarga. No se modifica nunca. |
| `processed/` | Particiones limpias en Parquet: `train.parquet`, `val.parquet`, `test.parquet` y `categorias.json`. |
| `external/` | Artículos reales externos al dataset (arXiv, PubMed) para la evaluación final. |

## Dataset WOS-46985

- **Fuente:** Web of Science Dataset, Kowsari et al. (2017), publicado en [Mendeley Data](https://data.mendeley.com/datasets/9rw3vkcfy4/6).
- **Contenido:** 46.985 resúmenes en inglés, 7 dominios y 134 áreas temáticas.
- **Archivo principal:** `Meta-data/Data.xlsx`, con las columnas `Y1`, `Y2`, `Y`, `Domain`, `area`, `keywords` y `Abstract`.

### Cómo ubicarlo

1. Descarga el archivo comprimido desde el enlace anterior.
2. Descomprímelo dentro de `data/raw/`, de modo que quede:

```text
data/raw/WebOfScience/
├── Meta-data/Data.xlsx
├── WOS46985/
├── WOS11967/
└── WOS5736/
```

Este proyecto usa `Meta-data/Data.xlsx` (equivalente a `WOS46985/`).
