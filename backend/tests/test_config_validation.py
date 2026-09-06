import pytest
from pydantic import ValidationError

from app.models.simulation_config import SimulationConfig

BASE = {
    "company_context": "Test Co",
    "framework_description": "Testing names",
}


def make_config(**overrides):
    payload = {
        **BASE,
        "candidates": [{"name": "Option A"}, {"name": "Option B"}],
        "personas": [
            {"id": "a", "name": "A", "description": "d", "weight": 45},
            {"id": "b", "name": "B", "description": "d", "weight": 35},
            {"id": "c", "name": "C", "description": "d", "weight": 20},
        ],
    }
    payload.update(overrides)
    return SimulationConfig(**payload)


def test_weights_normalize_from_raw_percentages():
    config = make_config()
    weights = {p.id: p.normalized_weight for p in config.personas}
    assert weights["a"] == pytest.approx(0.45)
    assert weights["b"] == pytest.approx(0.35)
    assert weights["c"] == pytest.approx(0.20)


def test_weights_already_fractional_normalize_identically():
    config = make_config(
        personas=[
            {"id": "a", "name": "A", "description": "d", "weight": 0.45},
            {"id": "b", "name": "B", "description": "d", "weight": 0.35},
            {"id": "c", "name": "C", "description": "d", "weight": 0.20},
        ]
    )
    weights = {p.id: p.normalized_weight for p in config.personas}
    assert weights["a"] == pytest.approx(0.45)
    assert weights["c"] == pytest.approx(0.20)


def test_rejects_non_positive_weight_sum():
    with pytest.raises(ValidationError, match="positive number"):
        make_config(
            personas=[
                {"id": "a", "name": "A", "description": "d", "weight": 0},
                {"id": "b", "name": "B", "description": "d", "weight": 0},
            ]
        )


def test_rejects_fewer_than_two_candidates():
    with pytest.raises(ValidationError):
        make_config(candidates=[{"name": "Only One"}])


def test_rejects_more_than_five_candidates():
    with pytest.raises(ValidationError):
        make_config(candidates=[{"name": f"Option {i}"} for i in range(6)])


def test_rejects_more_than_five_personas():
    with pytest.raises(ValidationError):
        make_config(
            personas=[
                {"id": f"p{i}", "name": f"P{i}", "description": "d", "weight": 1}
                for i in range(6)
            ]
        )


def test_allows_exactly_five_candidates_and_personas():
    config = make_config(
        candidates=[{"name": f"Option {i}"} for i in range(5)],
        personas=[
            {"id": f"p{i}", "name": f"P{i}", "description": "d", "weight": 1}
            for i in range(5)
        ],
    )
    assert len(config.candidates) == 5
    assert len(config.personas) == 5
