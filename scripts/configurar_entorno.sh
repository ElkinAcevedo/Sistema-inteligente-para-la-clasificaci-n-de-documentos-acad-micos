#!/usr/bin/env bash
# Prepara el entorno de desarrollo completo (Linux / macOS).
# Uso: ./scripts/configurar_entorno.sh   (desde la raíz del repositorio)
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v uv >/dev/null 2>&1; then
  echo "Falta uv. Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1
fi

echo "==> Python 3.12 y entorno virtual (.venv)"
uv venv --clear --python 3.12 .venv

echo "==> Dependencias de Python (ml + backend)"
uv pip install --python .venv -e "ml[dev,notebooks]" -e "backend[dev]"

echo "==> Recursos de lenguaje (spaCy y NLTK)"
SPACY=$(.venv/bin/python -c "import spacy; a, b, *_ = spacy.__version__.split('.'); print(f'{a}.{b}.0')")
uv pip install --python .venv "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-${SPACY}/en_core_web_sm-${SPACY}-py3-none-any.whl"
.venv/bin/python -m nltk.downloader -q stopwords

echo "==> Frontend"
if command -v npm >/dev/null 2>&1; then npm --prefix frontend install; else echo "Aviso: falta Node.js, omito el frontend."; fi

[ -f backend/.env ] || cp backend/.env.example backend/.env

echo "Listo. Activa el entorno con: source .venv/bin/activate"
