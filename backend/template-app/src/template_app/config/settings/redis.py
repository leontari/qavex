"""
Redis runtime settings.

This module contains environment-driven Redis configuration used by
the application's infrastructure layer.

The settings defined here are responsible for configuring:
- Redis cache connectivity
- message broker integration
- distributed locks
- background task queues
- pub/sub communication

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes secrets
- CI/CD runtime injection

Supported Redis use cases:
- application caching
- Celery broker/backend
- rate limiting
- session storage
- distributed synchronization
- health monitoring

Security considerations:
    Production Redis instances should:
    - require authentication
    - avoid public network exposure
    - use private/internal networking
    - optionally enable TLS

Example:
    REDIS_URL=redis://redis:6379/0

Design principles:
    - strict typing
    - immutable runtime configuration
    - deployment portability
    - infrastructure isolation
"""

from __future__ import annotations

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

from template_app.config.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class RedisSettings(BaseSettings):
    """
    Runtime Redis configuration.

    This settings model defines Redis connectivity settings used across
    the application infrastructure layer.

    Attributes:
        REDIS_URL:
            Redis connection URL used for cache and messaging services.

    """

    REDIS_URL: RedisDsn = "redis://localhost:6379/0"

    model_config = COMMON_SETTINGS_CONFIG
