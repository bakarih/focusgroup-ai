from langgraph.graph import END, StateGraph

from app.graph.nodes.critic import critic_node
from app.graph.nodes.executor import executor_node
from app.graph.nodes.planner import planner_node
from app.models.state import SimulationState


def _has_more_phases(state: SimulationState) -> str:
    return "executor" if state["current_phase_index"] < len(state["phases"]) else "critic"


def build_graph():
    graph = StateGraph(SimulationState)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("critic", critic_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_conditional_edges(
        "executor",
        _has_more_phases,
        {"executor": "executor", "critic": "critic"},
    )
    graph.add_edge("critic", END)
    return graph.compile()
