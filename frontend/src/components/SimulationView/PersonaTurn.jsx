const PALETTE = ['#5b8def', '#e0705b', '#4caf82', '#c07be0', '#e0b64f']

function colorFor(personaId) {
  let hash = 0
  for (let i = 0; i < personaId.length; i += 1) {
    hash = (hash * 31 + personaId.charCodeAt(i)) % PALETTE.length
  }
  return PALETTE[Math.abs(hash) % PALETTE.length]
}

export function PersonaTurn({ turn }) {
  const label = turn.personaName || turn.personaId
  return (
    <div className="persona-turn" style={{ borderLeftColor: colorFor(turn.personaId) }}>
      <div className="persona-turn-header">
        <strong>{label}</strong>
        {turn.candidateName && <span className="candidate-tag">{turn.candidateName}</span>}
      </div>
      <p>{turn.content}</p>
    </div>
  )
}
