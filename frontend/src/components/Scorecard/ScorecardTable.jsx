const VECTOR_LABELS = {
  scope_coverage: 'Scope Coverage',
  corporate_safety: 'Corporate Safety',
  modern_edge: 'Modern Edge',
  storytelling_value: 'Storytelling Value',
}

export function ScorecardTable({ scorecard, personas }) {
  const sorted = [...scorecard].sort((a, b) => b.composite_score - a.composite_score)
  const vectorKeys = Object.keys(VECTOR_LABELS)
  const personaLabel = (id) => personas.find((p) => p.id === id)?.name || id

  return (
    <table className="scorecard-table">
      <thead>
        <tr>
          <th>Option</th>
          {vectorKeys.map((key) => (
            <th key={key}>{VECTOR_LABELS[key]}</th>
          ))}
          {personas.map((p) => (
            <th key={p.id}>{personaLabel(p.id)}</th>
          ))}
          <th>Composite</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((entry) => (
          <tr key={entry.candidate_name}>
            <td>{entry.candidate_name}</td>
            {vectorKeys.map((key) => (
              <td key={key}>{entry.vectors[key]}</td>
            ))}
            {personas.map((p) => (
              <td key={p.id}>{entry.persona_ratings[p.id]}</td>
            ))}
            <td>
              <strong>{entry.composite_score}</strong>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
