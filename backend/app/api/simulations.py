import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.models.simulation_config import SimulationConfig
from app.services.session_store import create_session, get_session

router = APIRouter()

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@router.post("/api/simulations")
async def create_simulation(config: SimulationConfig) -> dict:
    record = create_session(config)
    return {"session_id": record.session_id}


@router.get("/api/simulations/{session_id}")
async def get_simulation(session_id: str) -> dict:
    record = get_session(session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="session not found")
    return {
        "session_id": session_id,
        "status": record.state["status"],
        "state": record.state,
    }


@router.get("/api/examples/hiring-tool")
async def get_hiring_tool_example() -> dict:
    path = EXAMPLES_DIR / "hiring_tool_config.json"
    return json.loads(path.read_text())
