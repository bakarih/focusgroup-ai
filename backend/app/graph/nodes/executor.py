from langchain_core.runnables import RunnableConfig

from app.graph.formatting import format_candidates_list, format_turns
from app.graph.llm import get_chat_model
from app.graph.prompts import CROSS_EXAM_PROMPT, EXECUTOR_PROMPT
from app.models.state import SimulationState

DISAGREE_INSTRUCTION = (
    "Directly reference and challenge specific prior speakers by name where you "
    "disagree with them; do not simply agree."
)


async def _run_turn(state, config, emit, cfg, phase, persona, candidate_name, messages) -> dict:
    turn_index = len(state["turns"])
    await emit(
        {
            "type": "persona-turn-start",
            "phase_index": phase["phase_index"],
            "turn_index": turn_index,
            "persona_id": persona["id"],
            "candidate_name": candidate_name,
        }
    )
    model = get_chat_model(cfg.get("model_name")).with_config(
        tags=["focusgroup", f"phase-{phase['phase_index']}", persona["id"]],
        metadata={"session_id": state["session_id"]},
    )
    content = ""
    async for chunk in model.astream(messages):
        piece = chunk.content or ""
        content += piece
        if piece:
            await emit(
                {
                    "type": "persona-turn-token",
                    "turn_index": turn_index,
                    "persona_id": persona["id"],
                    "token": piece,
                }
            )
    turn = {
        "persona_id": persona["id"],
        "persona_name": persona["name"],
        "phase_index": phase["phase_index"],
        "turn_index": turn_index,
        "candidate_name": candidate_name,
        "content": content,
    }
    state["turns"].append(turn)
    await emit({"type": "persona-turn-complete", **turn})
    return turn


async def executor_node(state: SimulationState, config: RunnableConfig) -> SimulationState:
    emit = config["configurable"]["emit"]
    cfg = state["config"]
    phase = state["phases"][state["current_phase_index"]]
    await emit({"type": "phase-start", "phase_index": phase["phase_index"], "phase_name": phase["name"]})

    if phase["phase_index"] < 2:
        for candidate in cfg["candidates"]:
            prior_for_candidate: list[dict] = []
            for _round in range(cfg.get("phase1_turns_per_persona", 1)):
                for persona in cfg["personas"]:
                    messages = EXECUTOR_PROMPT.format_messages(
                        persona_name=persona["name"],
                        persona_description=persona["description"],
                        phase_name=phase["name"],
                        phase_guidance=phase["guidance"],
                        instruction=DISAGREE_INSTRUCTION,
                        company_context=cfg["company_context"],
                        candidate_name=candidate["name"],
                        prior_turns_text=format_turns(prior_for_candidate),
                    )
                    turn = await _run_turn(
                        state, config, emit, cfg, phase, persona, candidate["name"], messages
                    )
                    prior_for_candidate.append(turn)
    else:
        for _round in range(cfg.get("phase3_rounds", 2)):
            for persona in cfg["personas"]:
                messages = CROSS_EXAM_PROMPT.format_messages(
                    persona_name=persona["name"],
                    persona_description=persona["description"],
                    phase_name=phase["name"],
                    phase_guidance=phase["guidance"],
                    company_context=cfg["company_context"],
                    candidates_list=format_candidates_list(cfg["candidates"]),
                    transcript_text=format_turns(state["turns"]),
                )
                await _run_turn(state, config, emit, cfg, phase, persona, None, messages)

    await emit({"type": "phase-complete", "phase_index": phase["phase_index"]})
    state["current_phase_index"] += 1
    return state
