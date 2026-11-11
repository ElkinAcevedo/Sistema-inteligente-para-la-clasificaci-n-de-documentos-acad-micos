# Guía de contribución

Reglas de trabajo del equipo para mantener el repositorio ordenado y la rama `main` siempre funcional.

## Ramas

| Rama | Uso |
| --- | --- |
| `main` | Versión estable. Solo recibe cambios desde `develop` mediante *pull request*. |
| `develop` | Integración del trabajo en curso. |
| `feature/<descripcion-corta>` | Nueva funcionalidad. Ej: `feature/extraccion-pdf` |
| `fix/<descripcion-corta>` | Corrección de un error. |
| `docs/<descripcion-corta>` | Solo documentación. |
| `exp/<descripcion-corta>` | Experimentos de modelos y notebooks. |

Flujo: crea tu rama desde `develop` → haz commits pequeños → abre un *pull request* hacia `develop` → otro integrante lo revisa → se fusiona.

```bash
git switch develop
git pull
git switch -c feature/extraccion-pdf
```

## Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/es/) con la descripción en español y en imperativo:

```text
<tipo>(<alcance>): <descripción>
```

| Tipo | Cuándo |
| --- | --- |
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un error |
| `docs` | Documentación |
| `test` | Pruebas |
| `refactor` | Cambio de código sin cambiar el comportamiento |
| `chore` | Configuración, dependencias, tareas varias |
| `exp` | Experimentos de modelos |

Ejemplos:

```text
feat(extraccion): extraer texto de archivos PDF con PyMuPDF
fix(api): devolver 415 cuando el formato no es soportado
exp(svm): comparar C=0.5 y C=1.0 en validación
```

## Antes de abrir un *pull request*

- [ ] `ruff check backend ml` no muestra errores.
- [ ] `pytest` pasa en `ml/` y en `backend/`.
- [ ] Agregaste pruebas para el código nuevo.
- [ ] Si cambiaste la API, actualizaste los esquemas y la documentación.

GitHub Actions ejecuta estas verificaciones automáticamente en cada *pull request*.

## Estilo de código

- **Python:** PEP 8, verificado con `ruff` (configuración en `ruff.toml`). Líneas de hasta 100 caracteres.
- **Nombres:** en español para el dominio del problema (`clasificar_documento`, `area_tematica`) y en inglés solo cuando lo exige una librería.
- **Notebooks:** limpia las salidas antes de hacer commit si contienen datos pesados. Nómbralos `NN-autor-descripcion.ipynb`.
- **Datos y modelos:** nunca subas archivos de `data/` ni de `models/`; están en `.gitignore`.
