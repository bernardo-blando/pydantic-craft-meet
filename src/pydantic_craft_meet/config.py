"""Application configuration using pydantic-settings.

This module demonstrates the recommended pattern for configuration management.
Config values are loaded from environment variables with type validation.

Usage:
    from pydantic_craft_meet.config import config
    print(config.app_name)
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application config loaded from environment variables.

    Environment variables can be set directly or via a .env file.
    Variable names are case-insensitive and can use either format:
    - APP_NAME=MyApp
    - app_name=MyApp

    To add new configurations, simply add a new field:

        database_url: str = Field(
            default="sqlite:///./app.db",
            description="Database connection URL",
        )
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(
        default="Pydantic Craft Meet",
        description="Application name shown in docs",
    )
    app_version: str = Field(
        default="0.1.0",
        description="Application version",
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    # Server
    host: str = Field(
        default="0.0.0.0",
        description="Server host",
    )
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Server port",
    )


@lru_cache
def get_config() -> Config:
    """Get cached config instance.

    Using lru_cache ensures config values are only loaded once.

    Returns:
        The application config.
    """
    return Config()


# Convenience alias for direct import
config = get_config()
