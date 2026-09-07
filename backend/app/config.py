from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    langchain_tracing_v2: bool = False
    langchain_project: str = "focusgroup-ai-simulation"
    langchain_api_key: str = ""
    model_name: str = "claude-opus-5"
    port: int = 8000


settings = Settings()
