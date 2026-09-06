"""Small text-formatting helpers used to turn config/state dicts into readable
prompt text. Kept separate from prompts.py so the templates stay simple."""


def format_candidates_list(candidates: list[dict]) -> str:
    return ", ".join(c["name"] for c in candidates)


def format_personas_list(personas: list[dict]) -> str:
    return "; ".join(f"{p['id']}: {p['name']} — {p['description']}" for p in personas)


def format_turns(turns: list[dict]) -> str:
    if not turns:
        return "(none yet)"
    return "\n".join(f"- {t['persona_name']}: {t['content']}" for t in turns)
