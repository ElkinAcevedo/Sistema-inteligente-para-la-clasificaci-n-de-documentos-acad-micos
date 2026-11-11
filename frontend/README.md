# Frontend · Dashboard web

Aplicación de una sola página con **React 19 + TypeScript + Vite**, estilizada con **Tailwind CSS** y **shadcn/ui**, y con gráficos de **Recharts**.

## Vistas

| Vista | Contenido |
| --- | --- |
| Clasificar | Arrastrar y soltar PDF/DOCX/TXT, pegar texto, probar un ejemplo. |
| Resultado | Dominio y área con confianza, alternativas, términos clave, texto analizado y corrección. |
| Historial | Tabla paginada con filtros por dominio, fecha y estado. |
| Métricas | KPI del modelo activo, comparación de modelos y matriz de confusión. |

## Estructura

```text
frontend/
├── src/
│   ├── api/cliente.ts    # cliente HTTP y tipos del contrato de la API
│   ├── components/       # componentes reutilizables (Layout, tarjetas, gráficos)
│   ├── pages/            # Clasificar, Historial, Metricas (Resultado: pendiente)
│   ├── test/setup.ts     # configuración de Vitest + Testing Library
│   ├── App.tsx           # rutas (React Router)
│   └── index.css         # Tailwind CSS
├── vite.config.ts        # alias @/ → src/, proxy /api → :8000, Vitest
├── Dockerfile            # compila y sirve con Nginx
└── nginx.conf
```

Importa siempre con el alias `@/`, por ejemplo `import { api } from '@/api/cliente'`.

## Comandos

| Comando | Qué hace |
| --- | --- |
| `npm install` | Instala dependencias. |
| `npm run dev` | Servidor de desarrollo en <http://localhost:5173> (la API debe estar en el puerto 8000). |
| `npm run build` | Verifica tipos y compila a `dist/`. |
| `npm test` | Pruebas con Vitest. |
| `npm run lint` | Revisión de estilo con oxlint. |

Los componentes de shadcn/ui se agregarán a medida que se construyan las vistas (`npx shadcn@latest add <componente>`).
