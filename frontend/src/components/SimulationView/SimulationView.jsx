import { useSimulationSocket } from '../../hooks/useSimulationSocket.js'
import { ScorecardTable } from '../Scorecard/ScorecardTable.jsx'
import { ConnectionStatus } from './ConnectionStatus.jsx'
import { PhasePanel } from './PhasePanel.jsx'

export function SimulationView({ sessionId, personas }) {
  const result = useSimulationSocket(sessionId)

  return (
    <div className="simulation-view">
      <ConnectionStatus
        status={result.status}
        error={result.error}
        weightNormalization={result.weightNormalization}
      />

      {result.phases.map((phase) =>
        phase ? <PhasePanel key={phase.index} phase={phase} turnsById={result.turnsById} /> : null
      )}

      {result.scorecard && (
        <section className="scorecard-section">
          <h3>Final Scorecard</h3>
          <ScorecardTable scorecard={result.scorecard} personas={personas} />
        </section>
      )}
    </div>
  )
}
