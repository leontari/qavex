"""
Aggregated runtime application settings.

This module composes all environment-driven configuration models into
a single unified application settings object.

The settings system is based on Pydantic Settings and supports:
- environment variables
- .env files
- Docker runtime configuration
- Kubernetes secrets/config maps
- CI/CD environment injection
- bare-metal deployments
- wheel/package installations

This module MUST contain only runtime/environment-driven configuration.

Examples:
    - application environment
    - debug mode
    - database configuration
    - Redis configuration
    - JWT configuration
    - CORS configuration
    - observability configuration
    - external service integration

This module MUST NOT contain:
    - static constants
    - immutable route definitions
    - compile-time metadata
    - framework-independent constants

Static application configuration must be defined in:
    template_app.config.app

Design principles:
    - strict typing
    - immutable runtime configuration
    - modular settings composition
    - deployment portability
    - centralized configuration access
    - environment isolation
"""

from __future__ import annotations

from template_app.config.settings.base import BaseAppSettings
from template_app.config.settings.cors import CORSSettings
from template_app.config.settings.database import DatabaseSettings
from template_app.config.settings.jwt import JWTSettings
from template_app.config.settings.redis import RedisSettings


class Settings(
    BaseAppSettings,
    DatabaseSettings,
    RedisSettings,
    JWTSettings,
    CORSSettings,
):
    """
    Aggregated runtime application settings.

    This class combines all modular settings definitions into a single
    strongly-typed runtime configuration object used across the application.

    The settings object provides centralized access to:
    - application runtime configuration
    - infrastructure integration settings
    - security configuration
    - observability configuration
    - deployment-specific runtime behavior

    The configuration values are loaded from:
    - environment variables
    - .env files
    - container orchestration systems
    - CI/CD runtime environments

    Inherited settings groups:
        BaseAppSettings:
            Core application runtime settings.

        DatabaseSettings:
            Database connectivity configuration.

        RedisSettings:
            Redis cache/message broker configuration.

        JWTSettings:
            Authentication and token configuration.

        CORSSettings:
            Cross-origin resource sharing configuration.
    """


settings = Settings()

"""
Singleton application settings instance.

This object should be used as the primary access point for all
runtime configuration throughout the application.

Example:
    from template_app.config.settings import settings

    database_url = settings.DATABASE_URL
"""

__all__ = [
    "Settings",
    "settings",
]
