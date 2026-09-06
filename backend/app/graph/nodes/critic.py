from langchain_core.runnables import RunnableConfig

from app.graph.formatting import format_candidates_list, format_personas_list, format_turns
from app.graph.llm import get_chat_model
from app.graph.prompts import CRITIC_PROMPT
from app.models.scorecard_schema import ScorecardResponseSchema
from app.models.state import SimulationState

VECTOR_KEYS = ["scope_coverage", "corporate_safety", "modern_edge", "storytelling_value"]


def render_markdown(scorecard: list[dict]) -> str:
    header = "| Candidate | " + " | ".join(VECTOR_KEYS) + " | Composite |"
    sep = "|---" * (len(VECTOR_KEYS) + 2) + "|"
    rows = []
    for entry in sorted(scorecard, key=lambda e: e["composite_score"], reverse=True):
        vectors = " | ".join(str(entry["vectors"].get(k, "")) for k in VECTOR_KEYS)
        rows.append(f"| {entry['candidate_name']} | {vectors} | {entry['composite_score']} |")
    return "\n".join([header, sep, *rows])


async def critic_node(state: SimulationState, config: RunnableConfig) -> SimulationState:
    emit = config["configurable"]["emit"]
    cfg = state["config"]

    structured_model = get_chat_model(cfg.get("model_name")).with_structured_output(
        ScorecardResponseSchema
    )
    result = await structured_model.ainvoke(
        CRITIC_PROMPT.format_messages(
            company_context=cfg["company_context"],
            candidates_list=format_candidates_list(cfg["candidates"]),
            personas_list=format_personas_list(cfg["personas"]),
            transcript_text=format_turns(state["turns"]),
        )
    )

    scorecard = []
    for entry in result.candidates:
        composite = sum(
            entry.persona_ratings.get(p["id"], 0) * p["normalized_weight"] for p in cfg["personas"]
        )
        scorecard.append(
            {
                "candidate_name": entry.candidate_name,
                "vectors": entry.vectors,
                "persona_ratings": entry.persona_ratings,
                "composite_score": round(composite, 2),
            }
        )

    state["scorecard"] = scorecard
    state["status"] = "done"
    await emit({"type": "scorecard-ready", "scorecard": scorecard, "markdown": render_markdown(scorecard)})
    await emit({"type": "done"})
    return state
