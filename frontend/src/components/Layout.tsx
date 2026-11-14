import { useEffect, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { api } from '@/api/cliente'

const enlaces = [
  { a: '/', texto: 'Clasificar' },
  { a: '/historial', texto: 'Historial' },
  { a: '/metricas', texto: 'Métricas' },
]

export function Layout() {
  const [apiActiva, setApiActiva] = useState<boolean | null>(null)

  useEffect(() => {
    api.salud().then(() => setApiActiva(true)).catch(() => setApiActiva(false))
  }, [])

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <aside className="flex w-56 flex-col border-r border-slate-200 bg-white p-4">
        <p className="mb-6 px-2 text-lg font-semibold" title="Sistema Inteligente de Clasificación de Documentos Académicos">
          SICDA
        </p>
        <nav className="flex flex-col gap-1">
          {enlaces.map(({ a, texto }) => (
            <NavLink
              key={a}
              to={a}
              end
              className={({ isActive }) =>
                `rounded-md px-3 py-2 text-sm ${isActive ? 'bg-indigo-50 font-semibold text-indigo-700' : 'text-slate-600 hover:bg-slate-100'}`
              }
            >
              {texto}
            </NavLink>
          ))}
        </nav>
        <p className="mt-auto px-2 text-xs text-slate-500">
          API: {apiActiva === null ? 'comprobando…' : apiActiva ? 'activa' : 'sin conexión'}
        </p>
      </aside>
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  )
}
