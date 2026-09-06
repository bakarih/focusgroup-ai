from typing import TypedDict


class PersonaTurn(TypedDict):
    persona_id: str
    persona_name: str
    phase_index: int
    turn_index: int
    candidate_name: str | None
    content: str


class PhaseDefinition(TypedDict):
    phase_index: int
    name: str
    guidance: str


class ScorecardEntry(TypedDict):
    candidate_name: str
    vectors: dict[str, int]
    persona_ratings: dict[str, int]
    composite_score: float


class SimulationState(TypedDict):
    config: dict
    session_id: str
    phases: list[PhaseDefinition]
    current_phase_index: int
    turns: list[PersonaTurn]
    scorecard: list[ScorecardEntry] | None
    status: str
    error: str | None


PHASE_NAMES = [
    "First Impressions & Domain Recognition",
    "Friction, Safety & Trust",
    "The Verdict",
]
