"""
Static application configuration.

This module contains immutable, non-environment-driven configuration
values used across the application.

The configuration defined here is considered compile-time/static
configuration and must remain identical across all deployment targets:
- local development
- automated testing
- CI pipelines
- Docker environments
- Kubernetes clusters
- bare-metal installations
- wheel/package installations

This module is intended only for:
- static application metadata
- API route prefixes
- documentation routes
- internal constants
- immutable defaults
- framework-independent static values

This module MUST NOT contain:
- environment variables
- secrets
- database credentials
- Redis connection settings
- JWT configuration
- runtime infrastructure configuration

All environment-driven runtime settings MUST be defined in:
    template_app.config.settings

Design principles:
    - immutable configuration
    - strict typing
    - deployment independence
    - runtime safety
    - deterministic defaults
"""

from __future__ import annotations

from dataclasses import dataclass

from template_app._version import (
    __commit_id__,
    __version__,
)


@dataclass(frozen=True, slots=True)
class AppConfig:
    """
    Static immutable application configuration.

    This dataclass contains application-wide static constants that
    do not depend on runtime environment variables or deployment
    infrastructure.

    Attributes:
        APP_NAME:
            Internal application identifier.

        APP_TITLE:
            Human-readable application title.

        APP_DESCRIPTION:
            Short application description.

        APP_VERSION:
            Application version generated from VCS metadata.

        APP_COMMIT_SHA:
            Git commit SHA generated during build process.

        API_V1_PREFIX:
            Base prefix for version 1 API routes.

        DOCS_URL:
            Swagger/OpenAPI documentation endpoint.

        REDOC_URL:
            ReDoc documentation endpoint.

        OPENAPI_URL:
            OpenAPI schema endpoint.

        HEALTH_PATH:
            General health-check endpoint.

        LIVENESS_PATH:
            Kubernetes/container liveness probe endpoint.

        READINESS_PATH:
            Kubernetes/container readiness probe endpoint.

        METRICS_PATH:
            Metrics exposition endpoint.

        DEFAULT_PAGE_SIZE:
            Default pagination page size.

        MAX_PAGE_SIZE:
            Maximum allowed pagination page size.

        PASSWORD_MIN_LENGTH:
            Minimum allowed password length.

        REQUEST_TIMEOUT_SECONDS:
            Default application request timeout.

    """

    #######################
    # Application metadata
    #######################

    APP_NAME: str = "template-app"

    APP_TITLE: str = "Template App Service"

    APP_DESCRIPTION: str = "FastAPI template"

    # Auto-generated from VCS metadata
    APP_VERSION: str = __version__

    APP_COMMIT_SHA: str | None = __commit_id__

    # =========================================================================
    # API
    # =========================================================================

    API_V1_PREFIX: str = "/api/v1"

    # =========================================================================
    # Documentation routes
    # =========================================================================

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    # =========================================================================
    # Health and observability
    # =========================================================================

    HEALTH_PATH: str = "/health"

    LIVENESS_PATH: str = "/health/live"

    READINESS_PATH: str = "/health/ready"

    METRICS_PATH: str = "/metrics"

    # =========================================================================
    # Pagination
    # =========================================================================

    DEFAULT_PAGE_SIZE: int = 20

    MAX_PAGE_SIZE: int = 100

    # =========================================================================
    # Security defaults
    # =========================================================================

    PASSWORD_MIN_LENGTH: int = 8

    # =========================================================================
    # Runtime defaults
    # =========================================================================

    REQUEST_TIMEOUT_SECONDS: int = 30


config = AppConfig()
