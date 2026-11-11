import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import { Clasificar } from '@/pages/Clasificar'
import { Historial } from '@/pages/Historial'
import { Metricas } from '@/pages/Metricas'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Clasificar />} />
          <Route path="historial" element={<Historial />} />
          <Route path="metricas" element={<Metricas />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
