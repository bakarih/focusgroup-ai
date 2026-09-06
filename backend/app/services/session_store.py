import asyncio
import uuid

from app.models.simulation_config import SimulationConfig
from app.models.state import SimulationState


class SessionRecord:
    def __init__(self, session_id: str, config: dict):
        self.session_id = session_id
        self.config = config
        self.state: SimulationState = {
            "config": config,
            "session_id": session_id,
            "phases": [],
            "current_phase_index": 0,
            "turns": [],
            "scorecard": None,
            "status": "planning",
            "error": None,
        }
        self.event_log: list[dict] = []
        self.subscribers: list[asyncio.Queue] = []
        self.task: asyncio.Task | None = None

    async def emit(self, event: dict) -> None:
        self.event_log.append(event)
        for queue in list(self.subscribers):
            await queue.put(event)


SESSIONS: dict[str, SessionRecord] = {}


def get_session(session_id: str) -> SessionRecord | None:
    return SESSIONS.get(session_id)


def create_session(config: SimulationConfig) -> SessionRecord:
    session_id = str(uuid.uuid4())
    record = SessionRecord(session_id, config.model_dump())

    raw_total = sum(p.weight for p in config.personas)
    if abs(raw_total - 1.0) > 1e-9:
        record.event_log.append(
            {
                "type": "config-normalized",
                "raw_weights": {p.id: p.weight for p in config.personas},
                "normalized_weights": {p.id: round(p.normalized_weight, 4) for p in config.personas},
            }
        )

    SESSIONS[session_id] = record
    record.task = asyncio.create_task(run_simulation_task(record))
    return record


async def run_simulation_task(record: SessionRecord) -> None:
    from app.graph.build_graph import build_graph

    await record.emit({"type": "session-status", "status": "planning"})
    try:
        graph = build_graph()
        final_state = await graph.ainvoke(
            record.state,
            config={"configurable": {"emit": record.emit}},
        )
        record.state = final_state
    except Exception as exc:  # noqa: BLE001 - surface any failure to the client
        record.state["status"] = "error"
        record.state["error"] = str(exc)
        await record.emit({"type": "error", "message": str(exc)})
