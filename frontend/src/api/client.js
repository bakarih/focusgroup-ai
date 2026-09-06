const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'

export async function createSimulation(config) {
  const response = await fetch(`${API_BASE_URL}/api/simulations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  })
  if (!response.ok) {
    const detail = await response.text()
    throw new Error(`Failed to create simulation: ${detail}`)
  }
  return response.json()
}

export async function fetchExampleConfig() {
  const response = await fetch(`${API_BASE_URL}/api/examples/hiring-tool`)
  if (!response.ok) {
    throw new Error('Failed to fetch example config')
  }
  return response.json()
}

export function wsUrl(sessionId) {
  return `${WS_BASE_URL}/ws/simulations/${sessionId}`
}
