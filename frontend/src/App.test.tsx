import { render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import App from '@/App'

afterEach(() => vi.restoreAllMocks())

test('muestra la navegación principal', () => {
  vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('sin API'))
  render(<App />)
  expect(screen.getByRole('link', { name: 'Clasificar' })).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Métricas' })).toBeInTheDocument()
})
