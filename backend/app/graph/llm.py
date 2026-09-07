"""The single seam for LLM instantiation.

Every node must call get_chat_model() instead of importing ChatAnthropic directly —
this is what lets tests monkeypatch a fake model in and run the whole graph
with no network access / API key. It's also what makes swapping providers a
one-file change: this used to build a ChatOpenAI, and became this without
touching any node, prompt, or test.
"""

from langchain_anthropic import ChatAnthropic

from app.config import settings


def get_chat_model(model_name: str | None = None) -> ChatAnthropic:
    return ChatAnthropic(
        model=model_name or settings.model_name,
        api_key=settings.anthropic_api_key,
        max_tokens=2048,
        streaming=True,
    )
