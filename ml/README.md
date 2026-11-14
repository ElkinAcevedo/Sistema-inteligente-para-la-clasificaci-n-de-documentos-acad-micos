# ML · paquete `clasificador_ml`

Código de aprendizaje automático: preparación del dataset, preprocesamiento de texto, entrenamiento, evaluación y exportación de modelos.

El paquete se instala en modo editable y lo importan **tanto los scripts de entrenamiento como la API**. Así el texto que llega en producción se procesa exactamente igual que el texto con el que se entrenó.

## Módulos

| Módulo | Responsabilidad | Fase |
| --- | --- | --- |
| `rutas.py` | Rutas estándar del repositorio (`data/`, `models/`, `configs/`). | — |
| `configuracion.py` | Cargar un YAML de `configs/` combinado con `base.yaml`. | — |
| `datos.py` | Cargar WOS-46985, limpiar, generar `categorias.json` y dividir 70/15/15. | I |
| `preprocesamiento.py` | Normalización, *stopwords* y lematización en inglés. | II |
| `jerarquico.py` | Clasificador de dominio + un clasificador de área por dominio. | III |
| `entrenamiento.py` | Entrenar cada modelo candidato a partir de un archivo de `configs/`. | III |
| `evaluacion.py` | Precisión, recall, F1 y matrices de confusión por nivel. | III |

## Preparar el dataset (Fase I)

Con el dataset en `data/raw/` (ver [`data/README.md`](../data/README.md)):

```bash
python -m clasificador_ml.datos
```

Genera `data/processed/{train,val,test}.parquet` y `categorias.json`. Las reglas de etiquetado están en [ADR 0002](../docs/decisiones/0002-etiquetas-wos.md).

## Configuraciones

`configs/base.yaml` define la semilla, la partición y los parámetros de TF-IDF. Cada modelo tiene su archivo:

- `naive_bayes.yaml`: Complement Naive Bayes (línea base)
- `svm.yaml`: SVM lineal calibrado
- `distilbert.yaml`: DistilBERT con *fine-tuning* (se entrena en Google Colab)

## Instalación

El script `scripts/configurar_entorno.sh` (o `.ps1`) ya instala el paquete con `dev` y `notebooks`, el modelo `en_core_web_sm` de spaCy y las *stopwords* de NLTK.

Para entrenar DistilBERT en tu equipo (opcional, descarga varios GB; lo normal es usar Google Colab):

```bash
uv pip install -e "ml[transformers]"
```

Para abrir los notebooks:

```bash
jupyter lab notebooks/
```

## Pruebas

```bash
pytest ml/tests
```
