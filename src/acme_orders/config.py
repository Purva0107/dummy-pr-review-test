"""Application settings loaded from environment."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ACME_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "local"
    api_key: str = "dev-acme-orders-key-change-me"
    database_url: str = "sqlite:///./data/orders.db"
    default_tax_bps: int = 825  # 8.25%
    log_level: str = "INFO"
    service_name: str = "acme-orders-api"
    max_line_items: int = 50
    inventory_soft_hold_seconds: int = 900


@lru_cache
def get_settings() -> Settings:
    return Settings()
