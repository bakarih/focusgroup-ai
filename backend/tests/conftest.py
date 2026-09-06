import re
from types import SimpleNamespace

import pytest

from app.models.scorecard_schema import VECTOR_KEYS, ScorecardCandidateResult, ScorecardResponseSchema


class FakeStructuredModel:
    """Fakes with_structured_output(...).ainvoke(...) for the critic node.

    Parses the candidate/persona lists straight out of the rendered prompt text
    (rather than hardcoding a scenario) so it works for any SimulationConfig a
    test throws at it.
    """

    async def ainvoke(self, messages) -> ScorecardResponseSchema:
        human_text = messages[-1].content

        candidates_match = re.search(r"Options under evaluation: (.+)", human_text)
        candidate_names = (
            [c.strip() for c in candidates_match.group(1).split(",")] if candidates_match else ["Option A"]
        )

        personas_match = re.search(r"Personas \(id: name — description\): (.+)", human_text)
        persona_ids = []
        if personas_match:
            for part in personas_match.group(1).split(";"):
                persona_id = part.strip().split(":")[0].strip()
                if persona_id:
                    persona_ids.append(persona_id)
        if not persona_ids:
            persona_ids = ["persona_1"]

        results = []
        for i, name in enumerate(candidate_names):
            vectors = {key: 5 + (i % 3) for key in VECTOR_KEYS}
            ratings = {pid: 6 + (j % 3) for j, pid in enumerate(persona_ids)}
            results.append(
                ScorecardCandidateResult(candidate_name=name, vectors=vectors, persona_ratings=ratings)
            )
        return ScorecardResponseSchema(candidates=results)


class FakeChatModel:
    """Fakes a LangChain chat model for planner/executor plain-text calls."""

    def with_config(self, **kwargs) -> "FakeChatModel":
        return self

    def with_structured_output(self, schema) -> FakeStructuredModel:
        return FakeStructuredModel()

    async def ainvoke(self, messages) -> SimpleNamespace:
        return SimpleNamespace(content="This is a mock panelist turn.")

    async def astream(self, messages):
        for word in "This is a mock panelist turn.".split(" "):
            yield SimpleNamespace(content=word + " ")


@pytest.fixture(autouse=True)
def fake_llm(monkeypatch):
    """Every test gets a fake LLM everywhere a node reaches for get_chat_model() —
    no network access or OPENAI_API_KEY is ever required to run this suite."""
    factory = lambda *args, **kwargs: FakeChatModel()
    monkeypatch.setattr("app.graph.nodes.planner.get_chat_model", factory)
    monkeypatch.setattr("app.graph.nodes.executor.get_chat_model", factory)
    monkeypatch.setattr("app.graph.nodes.critic.get_chat_model", factory)
