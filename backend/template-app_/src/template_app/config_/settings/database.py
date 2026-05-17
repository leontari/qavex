"""
Database runtime settings.

This module contains environment-driven database configuration used by
the application's persistence layer.

The settings defined here are responsible for configuring:
- SQLAlchemy database connectivity
- async database drivers
- query logging behavior
- ORM runtime integration

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations

Supported database drivers:
- PostgreSQL + asyncpg
- PostgreSQL + psycopg
- other SQLAlchemy-compatible drivers

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes secrets
- CI/CD runtime injection

Security considerations:
    Database credentials should never be hardcoded in production.

    Production deployments should provide DATABASE_URL through:
    - Kubernetes secrets
    - Docker secrets
    - CI/CD secret stores
    - infrastructure environment variables

Example:
    DATABASE_URL=postgresql+asyncpg://user:password@db:5432/app

Design principles:
    - strict typing
    - immutable runtime configuration
    - deployment portability
    - production-safe defaults

"""

from __future__ import annotations

from pydantic import (
    Field,
    PostgresDsn,
)
from pydantic_settings import BaseSettings

from template_app.config_.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class DatabaseSettings(BaseSettings):
    """
    Runtime database configuration.

    This settings model defines database connectivity and ORM-related
    runtime behavior for the application.

    Attributes:
        DATABASE_URL:
            SQLAlchemy-compatible PostgreSQL connection URL.

        DATABASE_ECHO:
            Enables SQLAlchemy query logging and SQL debugging output.

    """

    DATABASE_URL: PostgresDsn = Field(
        default=(
            "postgresql+asyncpg://user:password@localhost:5432/template_app"
        ),
    )

    DATABASE_ECHO: bool = False

    model_config = COMMON_SETTINGS_CONFIG
