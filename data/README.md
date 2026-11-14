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

> El `.zip` de Mendeley no trae la carpeta `WebOfScience/`: créala y descomprime dentro de ella.

En Linux/macOS se puede hacer todo desde la terminal:

```bash
mkdir -p data/raw/WebOfScience && cd data/raw/WebOfScience
curl -L -o wos.zip "https://data.mendeley.com/public-files/datasets/9rw3vkcfy4/files/c9ea673d-5542-44c0-ab7b-f1311f7d61df/file_downloaded"
unzip wos.zip && rm wos.zip
```

## Generar las particiones

```bash
python -m clasificador_ml.datos
```

Resultado en `processed/`:

| Archivo | Contenido |
| --- | --- |
| `train.parquet` | 32.888 documentos (70 %) |
| `val.parquet` | 7.047 documentos (15 %) |
| `test.parquet` | 7.048 documentos (15 %) |
| `categorias.json` | Jerarquía de 7 dominios y 136 áreas, con nombres, alias y tamaños |

Columnas de cada partición: `id_documento` (fila original del Excel), `texto` (resumen),
`palabras_clave`, `id_dominio`, `dominio`, `id_area`, `area` e `y_original` (`Y` del dataset).

Por qué son 136 áreas y no 134: ver [ADR 0002](../docs/decisiones/0002-etiquetas-wos.md).
