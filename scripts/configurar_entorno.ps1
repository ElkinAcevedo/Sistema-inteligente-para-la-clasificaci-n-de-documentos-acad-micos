# Prepara el entorno de desarrollo completo (Windows / PowerShell).
# Uso: .\scripts\configurar_entorno.ps1   (desde la raíz del repositorio)
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Host "Falta uv. Instálalo con: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`""
  exit 1
}

Write-Host "==> Python 3.12 y entorno virtual (.venv)"
uv venv --clear --python 3.12 .venv

Write-Host "==> Dependencias de Python (ml + backend)"
uv pip install --python .venv -e "ml[dev,notebooks]" -e "backend[dev]"

Write-Host "==> Recursos de lenguaje (spaCy y NLTK)"
$py = ".venv\Scripts\python.exe"
$spacy = & $py -c "import spacy; a, b, *_ = spacy.__version__.split('.'); print(f'{a}.{b}.0')"
uv pip install --python .venv "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-$spacy/en_core_web_sm-$spacy-py3-none-any.whl"
& $py -m nltk.downloader -q stopwords

Write-Host "==> Frontend"
if (Get-Command npm -ErrorAction SilentlyContinue) { npm --prefix frontend install } else { Write-Host "Aviso: falta Node.js, omito el frontend." }

if (-not (Test-Path backend\.env)) { Copy-Item backend\.env.example backend\.env }

Write-Host "Listo. Activa el entorno con: .venv\Scripts\Activate.ps1"
