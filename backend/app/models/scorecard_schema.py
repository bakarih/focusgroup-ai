from pydantic import BaseModel, Field

VECTOR_KEYS = ["scope_coverage", "corporate_safety", "modern_edge", "storytelling_value"]


class ScorecardCandidateResult(BaseModel):
    candidate_name: str
    vectors: dict[str, int] = Field(
        description="1-10 scores keyed by scope_coverage, corporate_safety, modern_edge, storytelling_value"
    )
    persona_ratings: dict[str, int] = Field(
        description="1-10 overall rating keyed by persona id"
    )


class ScorecardResponseSchema(BaseModel):
    candidates: list[ScorecardCandidateResult]
