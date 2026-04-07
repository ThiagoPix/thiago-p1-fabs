from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Music CRUD API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    mongodb_url: str = "mongodb://mongodb:27017"
    mongodb_db: str = "music_catalog"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
