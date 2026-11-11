# Modelos entrenados

Los artefactos `.joblib` **no se suben a GitHub**. Se generan con el pipeline de `ml/` o se comparten entre el equipo por otro medio (Drive o GitHub Releases).

## Convención de carpetas

```text
models/
└── <algoritmo>/<version>/
    ├── vectorizador.joblib     # TfidfVectorizer ajustado
    ├── dominio.joblib          # clasificador de nivel 1
    ├── areas/<dominio>.joblib  # un clasificador de nivel 2 por dominio
    ├── categorias.json         # jerarquía dominio → áreas
    └── metricas.json           # métricas en validación y prueba + hiperparámetros
```

Ejemplo: `models/svm/1.0.0/`. La API carga la versión marcada como activa al iniciar.
