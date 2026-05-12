"""
Static application configuration.

This module contains static, non-environment-driven configuration values.
Environment-driven settings MUST be defined in `template_app.config.settings`.
"""

from __future__ import annotations

from dataclasses import dataclass

from template_app._version import (
    __commit_id__,
    __version__,
)


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Static configuration values for the application."""

    # Application metadata
    APP_NAME: str = "template-app"
    APP_TITLE: str = "Template App Service"
    APP_DESCRIPTION: str = "FastAPI template"
    # Auto-generated from VCS
    APP_VERSION: str = __version__
    APP_COMMIT_SHA: str | None = __commit_id__

    # API
    API_V1_PREFIX: str = "/api/v1"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    # Health checks
    HEALTH_PATH: str = "/health"
    LIVENESS_PATH: str = "/health/live"
    READINESS_PATH: str = "/health/ready"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Security
    PASSWORD_MIN_LENGTH: int = 8

    # Timeouts
    REQUEST_TIMEOUT_SECONDS: int = 30


config = AppConfig()
