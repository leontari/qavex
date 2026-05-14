"""
Base contracts and shared models for the health plugin system.

This module defines:

- health status enums
- standardized health check result models
- the abstract plugin interface used by all health providers

The plugin system is designed for:

- Kubernetes readiness/liveness probes
- background refresh schedulers
- concurrent async execution
- dependency-aware health orchestration
- circuit breaker integration
- cached probe execution

All health providers must inherit from `HealthCheckPlugin`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class HealthStatus(StrEnum):
    """
    Health status values returned by health checks.

    Values:
        HEALTHY:
            Service or dependency is fully operational.

        DEGRADED:
            Service is operational but partially impaired.

        UNHEALTHY:
            Service is unavailable or non-functional.
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass(slots=True)
class HealthCheckResult:
    """
    Result returned by a health plugin execution.

    Attributes:
        name:
            Unique plugin name.

        status:
            Health status classification.

        latency_ms:
            Execution latency in milliseconds.

        details:
            Optional structured diagnostic payload.

        error:
            Optional error description.

        timestamp:
            Unix timestamp of check completion.

    """

    name: str
    status: HealthStatus
    latency_ms: float

    details: dict[str, Any] | None = None
    error: str | None = None
    timestamp: float | None = None


@dataclass(slots=True)
class RefreshPolicy:
    """
    Scheduling policy for a health plugin.

    Attributes:
        interval_seconds:
            Background refresh interval.

        timeout_seconds:
            Maximum execution timeout.

        critical:
            Whether the plugin affects overall readiness.

        cache_ttl_seconds:
            Cache validity duration.

    """

    interval_seconds: int = 10
    timeout_seconds: int = 5

    critical: bool = True

    cache_ttl_seconds: int = 15


class HealthCheckPlugin(ABC):
    """
    Abstract base class for all health plugins.

    Each plugin represents a single health provider such as:

    - PostgreSQL
    - Redis
    - Kafka
    - S3
    - external APIs

    Plugins are executed asynchronously by the health scheduler
    and may participate in dependency-aware orchestration.

    Attributes:
        name:
            Unique plugin identifier.

        dependencies:
            Names of plugins this plugin depends on.

        policy:
            Refresh and timeout configuration.

    """

    name: str

    dependencies: set[str] = field(default_factory=set)

    policy: RefreshPolicy = RefreshPolicy()

    @abstractmethod
    async def check(self) -> HealthCheckResult:
        """
        Execute the health check.

        Returns:
            HealthCheckResult:
                Structured plugin execution result.

        """
        raise NotImplementedError
