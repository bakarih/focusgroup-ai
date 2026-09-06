const MIN_PERSONAS = 1
const MAX_PERSONAS = 5

function slugify(name) {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

export function PersonaListEditor({ personas, onChange }) {
  const canAdd = personas.length < MAX_PERSONAS
  const canRemove = personas.length > MIN_PERSONAS
  const totalWeight = personas.reduce((sum, p) => sum + (Number(p.weight) || 0), 0)

  function updateField(index, field, value) {
    const next = [...personas]
    const updated = { ...next[index], [field]: value }
    if (field === 'name' && !next[index].id) {
      updated.id = slugify(value)
    }
    next[index] = updated
    onChange(next)
  }

  function addPersona() {
    if (canAdd) onChange([...personas, { id: '', name: '', description: '', weight: 0 }])
  }

  function removePersona(index) {
    if (canRemove) onChange(personas.filter((_, i) => i !== index))
  }

  return (
    <fieldset className="list-editor">
      <legend>
        ICPs / Personas ({personas.length} of {MAX_PERSONAS})
      </legend>
      {personas.map((persona, index) => {
        const weight = Number(persona.weight) || 0
        const share = totalWeight > 0 ? weight / totalWeight : 0
        return (
          <div className="list-editor-row persona-row" key={index}>
            <input
              type="text"
              placeholder="Persona name"
              value={persona.name}
              onChange={(e) => updateField(index, 'name', e.target.value)}
            />
            <input
              type="text"
              placeholder="What this persona cares about"
              value={persona.description}
              onChange={(e) => updateField(index, 'description', e.target.value)}
            />
            <input
              type="number"
              min="0"
              placeholder="Weight"
              value={persona.weight}
              onChange={(e) => updateField(index, 'weight', e.target.value)}
            />
            <span className="normalized-hint">→ {(share * 100).toFixed(0)}%</span>
            <button type="button" onClick={() => removePersona(index)} disabled={!canRemove}>
              Remove
            </button>
          </div>
        )
      })}
      <button type="button" onClick={addPersona} disabled={!canAdd}>
        + Add ICP
      </button>
      <p className="normalized-summary">
        Weights sum to {totalWeight} — will normalize to 100% automatically.
      </p>
    </fieldset>
  )
}
