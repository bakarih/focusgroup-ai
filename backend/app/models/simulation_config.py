from pydantic import BaseModel, Field, model_validator


class Persona(BaseModel):
    """An ICP (Ideal Customer Profile) that argues in the focus group."""

    id: str
    name: str
    description: str
    weight: float
    normalized_weight: float = 0.0


class Candidate(BaseModel):
    """One option under evaluation (e.g. a brand name)."""

    name: str


class SimulationConfig(BaseModel):
    company_context: str
    framework_description: str
    candidates: list[Candidate] = Field(min_length=2, max_length=5)
    personas: list[Persona] = Field(min_length=1, max_length=5)
    phase1_turns_per_persona: int = 1
    phase3_rounds: int = 2
    model_name: str | None = None

    @model_validator(mode="after")
    def normalize_weights(self) -> "SimulationConfig":
        total = sum(p.weight for p in self.personas)
        if total <= 0:
            raise ValueError("persona weights must sum to a positive number")
        for p in self.personas:
            p.normalized_weight = p.weight / total
        return self
