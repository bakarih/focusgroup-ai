const LABELS = {
  connecting: 'Connecting…',
  planning: 'Planning phases…',
  executing: 'Debate in progress…',
  critiquing: 'Scoring…',
  done: 'Complete',
  error: 'Error',
}

export function ConnectionStatus({ status, error, weightNormalization }) {
  return (
    <div className={`connection-status status-${status}`}>
      <span className="status-dot" />
      <span>{LABELS[status] || status}</span>
      {weightNormalization && (
        <span className="normalization-note">
          (weights normalized: {JSON.stringify(weightNormalization.raw_weights)} →{' '}
          {JSON.stringify(weightNormalization.normalized_weights)})
        </span>
      )}
      {error && <span className="error-text">{error}</span>}
    </div>
  )
}
