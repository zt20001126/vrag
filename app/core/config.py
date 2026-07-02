from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "vision-rag"
    API_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    UPLOAD_DIR: Path = Path("data/uploads")
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/vision_rag"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
