from enum import StrEnum


class EventType(StrEnum):
    """WebSocket event `type` values. Every event is a JSON object: {"type": ..., ...payload}."""

    SESSION_STATUS = "session-status"
    PHASE_PLANNED = "phase-planned"
    PHASE_START = "phase-start"
    PERSONA_TURN_START = "persona-turn-start"
    PERSONA_TURN_TOKEN = "persona-turn-token"
    PERSONA_TURN_COMPLETE = "persona-turn-complete"
    PHASE_COMPLETE = "phase-complete"
    CONFIG_NORMALIZED = "config-normalized"
    SCORECARD_READY = "scorecard-ready"
    ERROR = "error"
    DONE = "done"
