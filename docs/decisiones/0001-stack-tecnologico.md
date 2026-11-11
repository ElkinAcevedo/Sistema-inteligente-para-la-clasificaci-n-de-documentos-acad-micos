# 0001. Stack tecnológico

- **Estado:** aceptada
- **Fecha:** 2026-11-12

## Contexto

El sistema necesita PLN y aprendizaje automático, una API y un dashboard web, y debe poder levantarlo cualquier integrante en Windows, Linux o macOS.

## Decisión

- **Python 3.11** para el backend y el ML, con un paquete compartido (`clasificador_ml`) para que el preprocesamiento sea idéntico en entrenamiento y predicción.
- **FastAPI** para la API: validación con Pydantic y documentación OpenAPI automática.
- **scikit-learn** para TF-IDF, Naive Bayes y SVM; **Transformers + PyTorch** para DistilBERT.
- **SQLite + SQLAlchemy** para la persistencia.
- **React + TypeScript + Vite** con Tailwind CSS, shadcn/ui y Recharts para el dashboard.
- **Docker Compose** para levantar todo con un solo comando.

## Alternativas consideradas

- **Flask o Django** para la API: Flask requiere más piezas para validar y documentar; Django es más grande de lo necesario.
- **PostgreSQL:** innecesario para el volumen del proyecto; SQLAlchemy permite migrar después sin reescribir código.
- **Streamlit** para la interfaz: rápido para prototipos, pero limita el diseño del dashboard y no separa el frontend de la API.

## Consecuencias

El equipo trabaja en dos lenguajes (Python y TypeScript). A cambio, la API queda desacoplada de la interfaz y el contrato JSON está tipado en ambos lados.
