import pytest

from app.graph.build_graph import build_graph
from app.models.scorecard_schema import VECTOR_KEYS
from app.models.simulation_config import SimulationConfig


def make_tiny_config() -> SimulationConfig:
    return SimulationConfig(
        company_context="Test Co",
        framework_description="Testing two names with two personas",
        candidates=[{"name": "Option A"}, {"name": "Option B"}],
        personas=[
            {"id": "p1", "name": "Persona One", "description": "d", "weight": 60},
            {"id": "p2", "name": "Persona Two", "description": "d", "weight": 40},
        ],
        phase1_turns_per_persona=1,
        phase3_rounds=2,
    )


async def noop_emit(event: dict) -> None:
    return None


@pytest.mark.asyncio
async def test_graph_runs_end_to_end_and_produces_scorecard():
    config = make_tiny_config()
    initial_state = {
        "config": config.model_dump(),
        "session_id": "test-session",
        "phases": [],
        "current_phase_index": 0,
        "turns": [],
        "scorecard": None,
        "status": "planning",
        "error": None,
    }

    graph = build_graph()
    final_state = await graph.ainvoke(
        initial_state,
        config={"configurable": {"emit": noop_emit}},
    )

    assert len(final_state["phases"]) == 3
    assert final_state["status"] == "done"

    # Phases 1-2: personas x candidates x phase1_turns_per_persona each
    expected_per_early_phase = 2 * 2 * 1
    # Phase 3: personas x phase3_rounds
    expected_phase3 = 2 * 2
    expected_total = expected_per_early_phase * 2 + expected_phase3
    assert len(final_state["turns"]) == expected_total

    turns_phase_0 = [t for t in final_state["turns"] if t["phase_index"] == 0]
    assert len(turns_phase_0) == expected_per_early_phase

    scorecard = final_state["scorecard"]
    assert scorecard is not None
    assert {entry["candidate_name"] for entry in scorecard} == {"Option A", "Option B"}

    normalized = {p.id: p.normalized_weight for p in config.personas}
    for entry in scorecard:
        assert set(entry["vectors"].keys()) == set(VECTOR_KEYS)
        expected_composite = round(
            sum(entry["persona_ratings"][pid] * weight for pid, weight in normalized.items()), 2
        )
        assert entry["composite_score"] == pytest.approx(expected_composite)
