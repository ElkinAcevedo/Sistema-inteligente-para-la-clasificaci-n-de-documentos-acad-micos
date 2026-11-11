# Notebooks

Exploración y experimentos. El código que se vaya a reutilizar se pasa al paquete `ml/`; los notebooks solo lo importan.

## Convención de nombres

`NN-iniciales-descripcion.ipynb`, por ejemplo `01-eda-exploracion-wos.ipynb`.

## Notebooks previstos

| Notebook | Fase | Propósito |
| --- | --- | --- |
| `01-exploracion-wos.ipynb` | I | Distribución de clases, longitud de resúmenes, datos faltantes. |
| `02-preprocesamiento.ipynb` | II | Efecto de cada paso de limpieza sobre el vocabulario. |
| `03-modelos-clasicos.ipynb` | III | Naive Bayes y SVM con TF-IDF; búsqueda de hiperparámetros. |
| `04-distilbert-colab.ipynb` | III | *Fine-tuning* de DistilBERT en Google Colab. |
| `05-comparacion-modelos.ipynb` | III | Tabla comparativa final y elección del modelo activo. |
