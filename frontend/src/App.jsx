import { useState } from 'react'
import { ConfigForm } from './components/ConfigForm/ConfigForm.jsx'
import { SimulationView } from './components/SimulationView/SimulationView.jsx'

export default function App() {
  const [runningConfig, setRunningConfig] = useState(null)
  const [sessionId, setSessionId] = useState(null)

  function handleStart(config, newSessionId) {
    setRunningConfig(config)
    setSessionId(newSessionId)
  }

  function handleReset() {
    setRunningConfig(null)
    setSessionId(null)
  }

  return (
    <div className="app">
      <header>
        <h1>FocusGroup.AI</h1>
        <p className="tagline">Simulated stateful persona debates for naming and product decisions.</p>
      </header>

      {!sessionId && <ConfigForm onStart={handleStart} />}

      {sessionId && (
        <>
          <button type="button" className="reset-button" onClick={handleReset}>
            ← Start a new simulation
          </button>
          <SimulationView sessionId={sessionId} personas={runningConfig?.personas ?? []} />
        </>
      )}
    </div>
  )
}
