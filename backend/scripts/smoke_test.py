"""Manual end-to-end smoke test against a REAL running backend + real Anthropic API.

Requires:
  1. `uvicorn main:app --reload --port 8000` running in another terminal, with a
     real ANTHROPIC_API_KEY set in backend/.env.
  2. `pip install websockets` (already in requirements.txt) plus `httpx`.

Usage:
    python scripts/smoke_test.py
"""

import asyncio
import json

import httpx
import websockets

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

TINY_CONFIG = {
    "company_context": "Spectrum Hire (spectrumhire.ai), a multi-tool AI hiring suite.",
    "framework_description": "Quick smoke test of the simulation engine.",
    "candidates": [{"name": "Option A"}, {"name": "Option B"}],
    "personas": [
        {"id": "p1", "name": "Persona One", "description": "Cares about speed.", "weight": 60},
        {"id": "p2", "name": "Persona Two", "description": "Cares about trust.", "weight": 40},
    ],
    "phase1_turns_per_persona": 1,
    "phase3_rounds": 1,
}


async def main() -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/simulations", json=TINY_CONFIG)
        response.raise_for_status()
        session_id = response.json()["session_id"]
        print(f"Created session {session_id}")

    async with websockets.connect(f"{WS_URL}/ws/simulations/{session_id}") as ws:
        async for raw in ws:
            event = json.loads(raw)
            print(event["type"], {k: v for k, v in event.items() if k != "token"})
            if event["type"] == "scorecard-ready":
                print("\nFinal scorecard:\n" + event["markdown"])
            if event["type"] in ("done", "error"):
                break


if __name__ == "__main__":
    asyncio.run(main())
