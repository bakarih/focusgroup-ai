const MIN_CANDIDATES = 2
const MAX_CANDIDATES = 5

export function CandidateListEditor({ candidates, onChange }) {
  const canAdd = candidates.length < MAX_CANDIDATES
  const canRemove = candidates.length > MIN_CANDIDATES

  function updateName(index, name) {
    const next = [...candidates]
    next[index] = { ...next[index], name }
    onChange(next)
  }

  function addCandidate() {
    if (canAdd) onChange([...candidates, { name: '' }])
  }

  function removeCandidate(index) {
    if (canRemove) onChange(candidates.filter((_, i) => i !== index))
  }

  return (
    <fieldset className="list-editor">
      <legend>
        Options ({candidates.length} of {MAX_CANDIDATES})
      </legend>
      {candidates.map((candidate, index) => (
        <div className="list-editor-row" key={index}>
          <input
            type="text"
            placeholder={`Option ${index + 1} name`}
            value={candidate.name}
            onChange={(e) => updateName(index, e.target.value)}
          />
          <button type="button" onClick={() => removeCandidate(index)} disabled={!canRemove}>
            Remove
          </button>
        </div>
      ))}
      <button type="button" onClick={addCandidate} disabled={!canAdd}>
        + Add option
      </button>
    </fieldset>
  )
}
