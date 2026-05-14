"""
Redis health provider.

This module defines a runtime health plugin for validating Redis
availability and responsiveness.
"""

from __future__ import annotations

import time

from redis.asyncio import Redis

from template_app.health.plugins.base import (
    HealthCheckPlugin,
    HealthCheckResult,
    HealthStatus,
    RefreshPolicy,
)


class RedisHealthPlugin(HealthCheckPlugin):
    """Redis runtime health plugin."""

    name = "redis"

    policy = RefreshPolicy(
        interval_seconds=5,
        timeout_seconds=2,
        critical=True,
        cache_ttl_seconds=10,
    )

    def __init__(
        self,
        redis: Redis,
    ) -> None:
        """
        Initialize the Redis health plugin.

        Args:
            redis:
                Async Redis client.
        """
        self.redis = redis

    async def check(self) -> HealthCheckResult:
        """
        Validate Redis availability.

        Returns:
            HealthCheckResult:
                Redis health result.
        """
        started = time.perf_counter()

        try:
            await self.redis.ping()

        except Exception as exc:
            latency = (time.perf_counter() - started) * 1000

            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.UNHEALTHY,
                latency_ms=latency,
                error=str(exc),
            )

        latency = (time.perf_counter() - started) * 1000

        return HealthCheckResult(
            name=self.name,
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
        )
