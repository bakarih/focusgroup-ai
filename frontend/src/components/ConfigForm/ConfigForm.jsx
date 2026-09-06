import { useState } from 'react'
import { createSimulation, fetchExampleConfig } from '../../api/client.js'
import { CandidateListEditor } from './CandidateListEditor.jsx'
import { PersonaListEditor } from './PersonaListEditor.jsx'

const EMPTY_CONFIG = {
  company_context: '',
  framework_description: '',
  candidates: [{ name: '' }, { name: '' }],
  personas: [{ id: '', name: '', description: '', weight: 1 }],
  phase1_turns_per_persona: 1,
  phase3_rounds: 2,
}

export function ConfigForm({ onStart }) {
  const [config, setConfig] = useState(EMPTY_CONFIG)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  function updateField(field, value) {
    setConfig((prev) => ({ ...prev, [field]: value }))
  }

  async function loadExample() {
    try {
      const example = await fetchExampleConfig()
      setConfig(example)
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const { session_id: sessionId } = await createSimulation(config)
      onStart(config, sessionId)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="config-form" onSubmit={handleSubmit}>
      <button type="button" className="load-example" onClick={loadExample}>
        Load hiring-tool example
      </button>

      <label>
        Company context
        <textarea
          value={config.company_context}
          onChange={(e) => updateField('company_context', e.target.value)}
          required
        />
      </label>

      <label>
        What's being evaluated
        <textarea
          value={config.framework_description}
          onChange={(e) => updateField('framework_description', e.target.value)}
          required
        />
      </label>

      <CandidateListEditor
        candidates={config.candidates}
        onChange={(candidates) => updateField('candidates', candidates)}
      />

      <PersonaListEditor
        personas={config.personas}
        onChange={(personas) => updateField('personas', personas)}
      />

      {error && <p className="error-text">{error}</p>}

      <button type="submit" disabled={submitting}>
        {submitting ? 'Starting…' : 'Run focus group'}
      </button>
    </form>
  )
}
