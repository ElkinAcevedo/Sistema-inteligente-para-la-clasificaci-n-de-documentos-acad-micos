# Imagen de la API. Se construye desde la raíz del repositorio:
#   docker build -f backend/Dockerfile .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /srv

# Primero el paquete ML compartido, luego la API.
COPY ml/ ml/
COPY backend/ backend/
RUN pip install ./ml ./backend \
 && python -m spacy download en_core_web_sm \
 && python -m nltk.downloader -d /usr/local/share/nltk_data stopwords

WORKDIR /srv/backend
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
