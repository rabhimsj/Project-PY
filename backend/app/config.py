from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CampusMind AI"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "change-me-to-a-random-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    database_url: str = "sqlite:///./campusmind.db"
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_provider: str = "local"
    max_upload_size_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


settings = Settings()
