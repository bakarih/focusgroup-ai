import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.session_store import get_session

router = APIRouter()

TERMINAL_EVENT_TYPES = {"done", "error"}


@router.websocket("/ws/simulations/{session_id}")
async def simulation_ws(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()

    record = get_session(session_id)
    if record is None:
        await websocket.send_json({"type": "error", "message": "session not found"})
        await websocket.close()
        return

    queue: asyncio.Queue = asyncio.Queue()
    # Register before snapshotting so no event emitted concurrently is lost
    # between the two lines (no `await` separates them, so this is atomic
    # under asyncio's single-threaded event loop).
    record.subscribers.append(queue)
    replay = list(record.event_log)

    try:
        for event in replay:
            await websocket.send_json(event)

        if replay and replay[-1]["type"] in TERMINAL_EVENT_TYPES:
            return

        while True:
            event = await queue.get()
            await websocket.send_json(event)
            if event.get("type") in TERMINAL_EVENT_TYPES:
                break
    except WebSocketDisconnect:
        pass
    finally:
        if queue in record.subscribers:
            record.subscribers.remove(queue)
