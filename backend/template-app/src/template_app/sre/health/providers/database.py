"""
PostgreSQL health provider.

This module defines a runtime health plugin for validating database
availability and responsiveness.

The plugin is intended for:

- Kubernetes readiness probes
- scheduler-managed background checks
- degraded state propagation
- runtime dependency orchestration
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from sqlalchemy import text

from template_app.health.plugins.base import (
    HealthCheckPlugin,
    HealthCheckResult,
    HealthStatus,
    RefreshPolicy,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
    )


class DatabaseHealthPlugin(HealthCheckPlugin):
    """PostgreSQL runtime health plugin."""

    name = "postgresql"

    policy = RefreshPolicy(
        interval_seconds=5,
        timeout_seconds=3,
        critical=True,
        cache_ttl_seconds=10,
    )

    def __init__(
        self,
        engine: AsyncEngine,
    ) -> None:
        """
        Initialize the database health plugin.

        Args:
            engine:
                SQLAlchemy async engine instance.

        """
        self.engine = engine

    async def check(self) -> HealthCheckResult:
        """
        Validate database availability.

        Returns:
            HealthCheckResult:
                Database health result.

        """
        started = time.perf_counter()

        try:
            async with self.engine.connect() as connection:
                await connection.execute(
                    text("SELECT 1"),
                )

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
