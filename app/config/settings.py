from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AI Token Optimization & Cost Management Platform"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-flash-lite-latest"
    database_url: str = ""
    input_cost_per_million_tokens: float = 0.0
    output_cost_per_million_tokens: float = 0.0
    redis_url: str = ""
    cache_ttl_seconds: int = 3600
    max_context_tokens: int = 4096
    summary_trigger_tokens: int = 3000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance for reuse across requests."""

    return Settings()
