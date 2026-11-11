# Frontend · Dashboard web

Aplicación de una sola página con **React 18 + TypeScript + Vite**, estilizada con **Tailwind CSS** y **shadcn/ui**, y con gráficos de **Recharts**.

> El proyecto Vite se inicializa en la etapa de configuración del entorno.

## Vistas

| Vista | Contenido |
| --- | --- |
| Clasificar | Arrastrar y soltar PDF/DOCX/TXT, pegar texto, probar un ejemplo. |
| Resultado | Dominio y área con confianza, alternativas, términos clave, texto analizado y corrección. |
| Historial | Tabla paginada con filtros por dominio, fecha y estado. |
| Métricas | KPI del modelo activo, comparación de modelos y matriz de confusión. |

## Estructura prevista

```text
frontend/
├── src/
│   ├── api/          # cliente HTTP y tipos del contrato de la API
│   ├── components/   # componentes reutilizables (ui/ = shadcn)
│   ├── pages/        # Clasificar, Resultado, Historial, Metricas
│   ├── hooks/
│   └── lib/
└── public/
```

## Ejecutar (cuando esté inicializado)

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
```
