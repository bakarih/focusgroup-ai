import { PersonaTurn } from './PersonaTurn.jsx'

export function PhasePanel({ phase, turnsById }) {
  return (
    <section className={`phase-panel ${phase.complete ? 'complete' : ''} ${phase.active ? 'active' : ''}`}>
      <h3>
        Phase {phase.index + 1}: {phase.name}
      </h3>
      {phase.guidance && <p className="phase-guidance">{phase.guidance}</p>}
      <div className="phase-turns">
        {phase.turnIndexes.map((turnIndex) => {
          const turn = turnsById[turnIndex]
          return turn ? <PersonaTurn key={turnIndex} turn={turn} /> : null
        })}
      </div>
    </section>
  )
}
