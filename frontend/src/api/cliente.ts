// Cliente HTTP de la API. Las rutas son relativas: Vite las redirige a FastAPI en desarrollo.
const BASE = '/api/v1'

export interface RespuestaSalud {
  estado: string
  version: string
  modelo_activo: string | null
}

async function obtener<T>(ruta: string): Promise<T> {
  const respuesta = await fetch(`${BASE}${ruta}`)
  if (!respuesta.ok) throw new Error(`Error ${respuesta.status} en ${ruta}`)
  return respuesta.json() as Promise<T>
}

export const api = {
  salud: () => obtener<RespuestaSalud>('/salud'),
}
