"""
ClickHouse runtime settings.

This module contains environment-driven ClickHouse configuration used
for analytical workloads and high-performance OLAP queries.

The settings defined here control:
- ClickHouse connectivity
- authentication
- database selection
- transport security
- query execution behavior

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

Typical ClickHouse use cases:
- analytics pipelines
- metrics aggregation
- event storage
- observability data
- time-series analysis
- reporting systems

Security considerations:
    Production ClickHouse deployments should:
    - require authentication
    - restrict public network exposure
    - isolate analytics infrastructure
    - optionally enable TLS encryption

Example:
    CLICKHOUSE_HOST=clickhouse
    CLICKHOUSE_PORT=8123
    CLICKHOUSE_DATABASE=analytics

Design principles:
    - strict typing
    - immutable runtime configuration
    - deployment portability
    - infrastructure isolation
    - analytics scalability
"""

from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings

from template_app.config_.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class ClickHouseSettings(BaseSettings):
    """
    Runtime ClickHouse configuration.

    This settings model defines ClickHouse connectivity and runtime
    behavior for analytical workloads.

    Attributes:
        CLICKHOUSE_ENABLED:
            Enables ClickHouse integration.

        CLICKHOUSE_HOST:
            ClickHouse server hostname.

        CLICKHOUSE_PORT:
            ClickHouse HTTP/native interface port.

        CLICKHOUSE_DATABASE:
            Default ClickHouse database name.

        CLICKHOUSE_USERNAME:
            ClickHouse authentication username.

        CLICKHOUSE_PASSWORD:
            ClickHouse authentication password.

        CLICKHOUSE_SECURE:
            Enables secure TLS connections.
    """

    CLICKHOUSE_ENABLED: bool = False

    CLICKHOUSE_HOST: str = "localhost"

    CLICKHOUSE_PORT: int = 8123

    CLICKHOUSE_DATABASE: str = "default"

    CLICKHOUSE_USERNAME: str = "default"

    CLICKHOUSE_PASSWORD: SecretStr | None = None

    CLICKHOUSE_SECURE: bool = False

    model_config = COMMON_SETTINGS_CONFIG
