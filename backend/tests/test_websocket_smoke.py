from fastapi.testclient import TestClient

from main import app


def make_tiny_payload() -> dict:
    return {
        "company_context": "Test Co",
        "framework_description": "Testing via websocket",
        "candidates": [{"name": "Option A"}, {"name": "Option B"}],
        "personas": [
            {"id": "p1", "name": "Persona One", "description": "d", "weight": 60},
            {"id": "p2", "name": "Persona Two", "description": "d", "weight": 40},
        ],
        "phase1_turns_per_persona": 1,
        "phase3_rounds": 1,
    }


def test_websocket_streams_full_event_sequence_in_order():
    # Use TestClient as a context manager: it keeps one AnyIO portal alive for
    # the whole block, so the asyncio.create_task() started by the POST
    # handler keeps running and is observable by the later websocket_connect
    # call. Without `with`, each call can get its own short-lived portal and
    # the background task never gets a chance to progress.
    with TestClient(app) as client:
        response = client.post("/api/simulations", json=make_tiny_payload())
        assert response.status_code == 200
        session_id = response.json()["session_id"]

        event_types = []
        with client.websocket_connect(f"/ws/simulations/{session_id}") as websocket:
            while True:
                event = websocket.receive_json()
                event_types.append(event["type"])
                if event["type"] in ("done", "error"):
                    break

    assert "error" not in event_types
    # The 60/40 weights above aren't pre-normalized, so a config-normalized
    # event lands before session-status — assert presence/order, not position 0.
    assert "config-normalized" in event_types
    assert event_types.index("config-normalized") < event_types.index("session-status")
    assert event_types.count("phase-start") == 3
    assert event_types.count("phase-complete") == 3
    # personas(2) x candidates(2) x 1 round, for each of phases 1-2, plus personas(2) x 1 round for phase 3
    assert event_types.count("persona-turn-complete") == 2 * 2 * 1 * 2 + 2 * 1

    first_phase_start = event_types.index("phase-start")
    last_phase_complete = len(event_types) - 1 - event_types[::-1].index("phase-complete")
    scorecard_index = event_types.index("scorecard-ready")

    assert first_phase_start < last_phase_complete < scorecard_index
    assert event_types[-1] == "done"
