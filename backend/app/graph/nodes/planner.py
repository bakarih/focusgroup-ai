from langchain_core.runnables import RunnableConfig

from app.graph.formatting import format_candidates_list
from app.graph.llm import get_chat_model
from app.graph.prompts import PLANNER_PROMPT
from app.models.state import PHASE_NAMES, SimulationState


async def planner_node(state: SimulationState, config: RunnableConfig) -> SimulationState:
    emit = config["configurable"]["emit"]
    cfg = state["config"]

    phases = []
    for i, name in enumerate(PHASE_NAMES):
        model = get_chat_model(cfg.get("model_name"))
        result = await model.ainvoke(
            PLANNER_PROMPT.format_messages(
                company_context=cfg["company_context"],
                framework_description=cfg["framework_description"],
                candidates_list=format_candidates_list(cfg["candidates"]),
                phase_name=name,
            )
        )
        phase = {"phase_index": i, "name": name, "guidance": result.content}
        phases.append(phase)
        await emit({"type": "phase-planned", **phase})

    state["phases"] = phases
    state["current_phase_index"] = 0
    state["status"] = "executing"
    return state
