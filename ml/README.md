# ML · paquete `clasificador_ml`

Código de aprendizaje automático: preparación del dataset, preprocesamiento de texto, entrenamiento, evaluación y exportación de modelos.

El paquete se instala en modo editable y lo importan **tanto los scripts de entrenamiento como la API**. Así el texto que llega en producción se procesa exactamente igual que el texto con el que se entrenó.

## Módulos

| Módulo | Responsabilidad | Fase |
| --- | --- | --- |
| `rutas.py` | Rutas estándar del repositorio (`data/`, `models/`, `configs/`). | — |
| `datos.py` | Cargar WOS-46985, limpiar, generar `categorias.json` y dividir 70/15/15. | I |
| `preprocesamiento.py` | Normalización, *stopwords* y lematización en inglés. | II |
| `jerarquico.py` | Clasificador de dominio + un clasificador de área por dominio. | III |
| `entrenamiento.py` | Entrenar cada modelo candidato a partir de un archivo de `configs/`. | III |
| `evaluacion.py` | Precisión, recall, F1 y matrices de confusión por nivel. | III |

## Configuraciones

`configs/base.yaml` define la semilla, la partición y los parámetros de TF-IDF. Cada modelo tiene su archivo:

- `naive_bayes.yaml`: Complement Naive Bayes (línea base)
- `svm.yaml`: SVM lineal calibrado
- `distilbert.yaml`: DistilBERT con *fine-tuning* (se entrena en Google Colab)

## Instalación

```bash
pip install -e "ml[dev]"                 # mínimo
pip install -e "ml[dev,notebooks]"       # + Jupyter y gráficos
pip install -e "ml[transformers]"        # + PyTorch y Transformers (pesado)
python -m spacy download en_core_web_sm
```

## Pruebas

```bash
pytest ml/tests
```
