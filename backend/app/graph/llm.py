"""The single seam for LLM instantiation.

Every node must call get_chat_model() instead of importing ChatOpenAI directly —
this is what lets tests monkeypatch a fake model in and run the whole graph
with no network access / API key.
"""

from langchain_openai import ChatOpenAI

from app.config import settings


def get_chat_model(model_name: str | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name or settings.model_name,
        api_key=settings.openai_api_key,
        streaming=True,
    )
