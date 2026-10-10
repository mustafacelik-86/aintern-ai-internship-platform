"""
AIntern — Application Settings
Reads from .env file via pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",          # silently ignore unknown env vars (e.g. old keys)
    )

    # ── Groq ──────────────────────────────────────────────────────────────────
    # pydantic-settings v2 auto-maps field name → uppercase env var
    # e.g. groq_api_key → GROQ_API_KEY
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"

    # ── Supabase ──────────────────────────────────────────────────────────────
    supabase_url: str = ""
    supabase_anon_key: str = ""

    # ── App ───────────────────────────────────────────────────────────────────
    app_env: str = "development"
    log_level: str = "INFO"


# Single shared instance — import this everywhere
settings = Settings()
