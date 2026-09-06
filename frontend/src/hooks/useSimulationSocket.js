import { useEffect, useRef, useState } from 'react'
import { wsUrl } from '../api/client.js'

function initialResult() {
  return {
    status: 'connecting',
    phases: [],
    turnsById: {},
    scorecard: null,
    scorecardMarkdown: null,
    weightNormalization: null,
    error: null,
  }
}

function applyEvent(prev, event) {
  switch (event.type) {
    case 'session-status':
      return { ...prev, status: event.status }

    case 'config-normalized':
      return { ...prev, weightNormalization: event }

    case 'phase-planned': {
      const phases = [...prev.phases]
      phases[event.phase_index] = {
        index: event.phase_index,
        name: event.name,
        guidance: event.guidance,
        turnIndexes: [],
        active: false,
        complete: false,
      }
      return { ...prev, phases }
    }

    case 'phase-start': {
      const phases = [...prev.phases]
      const phase = phases[event.phase_index]
      if (phase) phases[event.phase_index] = { ...phase, active: true }
      return { ...prev, phases }
    }

    case 'persona-turn-start': {
      const turnsById = {
        ...prev.turnsById,
        [event.turn_index]: {
          turnIndex: event.turn_index,
          personaId: event.persona_id,
          candidateName: event.candidate_name ?? null,
          content: '',
        },
      }
      const phases = [...prev.phases]
      const phase = phases[event.phase_index]
      if (phase && !phase.turnIndexes.includes(event.turn_index)) {
        phases[event.phase_index] = { ...phase, turnIndexes: [...phase.turnIndexes, event.turn_index] }
      }
      return { ...prev, turnsById, phases }
    }

    case 'persona-turn-token': {
      const existing = prev.turnsById[event.turn_index]
      if (!existing) return prev
      return {
        ...prev,
        turnsById: {
          ...prev.turnsById,
          [event.turn_index]: { ...existing, content: existing.content + event.token },
        },
      }
    }

    case 'persona-turn-complete': {
      const existing = prev.turnsById[event.turn_index] || {}
      return {
        ...prev,
        turnsById: {
          ...prev.turnsById,
          [event.turn_index]: {
            ...existing,
            turnIndex: event.turn_index,
            personaId: event.persona_id,
            personaName: event.persona_name,
            candidateName: event.candidate_name ?? null,
            content: event.content,
          },
        },
      }
    }

    case 'phase-complete': {
      const phases = [...prev.phases]
      const phase = phases[event.phase_index]
      if (phase) phases[event.phase_index] = { ...phase, active: false, complete: true }
      return { ...prev, phases }
    }

    case 'scorecard-ready':
      return { ...prev, scorecard: event.scorecard, scorecardMarkdown: event.markdown }

    case 'error':
      return { ...prev, error: event.message, status: 'error' }

    case 'done':
      return { ...prev, status: 'done' }

    default:
      return prev
  }
}

/** Owns the WebSocket for one simulation session and reduces its event
 * stream into renderable state. Reconnects are intentionally out of scope
 * for v1 — a dropped connection just stops updating; refreshing re-runs the
 * whole replay-from-event-log flow via a fresh connection. */
export function useSimulationSocket(sessionId) {
  const [result, setResult] = useState(initialResult)
  const socketRef = useRef(null)

  useEffect(() => {
    if (!sessionId) return undefined

    setResult(initialResult())
    const socket = new WebSocket(wsUrl(sessionId))
    socketRef.current = socket

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setResult((prev) => applyEvent(prev, data))
    }
    socket.onerror = () => {
      setResult((prev) => ({ ...prev, error: prev.error || 'WebSocket connection error' }))
    }

    return () => {
      socket.close()
      socketRef.current = null
    }
  }, [sessionId])

  return result
}
