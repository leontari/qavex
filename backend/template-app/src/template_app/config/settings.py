"""
Application settings.

This module defines environment-driven configuration for the application.
Settings are loaded from environment variables and optional .env
files. This approach ensures consistent behavior across environments:
local development, Docker, CI, and wheel-based installations.

It's a place for Pydantic configs like:
* envs
* bd
* redis
* JWT
* CORS
* debug
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    ##############
    # Environment
    ##############

    APP_ENV: str = "dev"
    DEBUG: bool = False

    ##########
    # Logging
    ##########

    LOG_LEVEL: str = "INFO"

    ###########
    # Database
    ###########

    database_url: str = (
        "postgresql+asyncpg://user:password@localhost:5432/template_app"
    )
    database_echo: bool = False

    ########
    # Redis
    ########

    redis_url: str = "redis://localhost:6379/0"

    #######
    # CORS
    #######

    cors_allow_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    ######
    # JWT
    ######

    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    ###########################
    # Pydantic settings config
    ###########################

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
