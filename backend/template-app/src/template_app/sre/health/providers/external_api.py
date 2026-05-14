"""
External API health provider.

This module defines a runtime health plugin for validating third-party
HTTP API availability.

The plugin supports:

- degraded state propagation
- timeout isolation
- scheduler-managed execution
- Kubernetes readiness integration
"""

from __future__ import annotations

import time

import httpx

from template_app.health.plugins.base import (
    HealthCheckPlugin,
    HealthCheckResult,
    HealthStatus,
    RefreshPolicy,
)


class ExternalAPIHealthPlugin(HealthCheckPlugin):
    """External HTTP API runtime health plugin."""

    name = "external_api"

    policy = RefreshPolicy(
        interval_seconds=30,
        timeout_seconds=5,
        critical=False,
        cache_ttl_seconds=60,
    )

    def __init__(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> None:
        """
        Initialize the external API health plugin.

        Args:
            client:
                Async HTTP client.

            url:
                Target health endpoint URL.

        """
        self.client = client
        self.url = url

    async def check(self) -> HealthCheckResult:
        """
        Validate external API availability.

        Returns:
            HealthCheckResult:
                External API health result.

        """
        started = time.perf_counter()

        try:
            response = await self.client.get(self.url)

            response.raise_for_status()

        except Exception as exc:
            latency = (time.perf_counter() - started) * 1000

            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.DEGRADED,
                latency_ms=latency,
                error=str(exc),
            )

        latency = (time.perf_counter() - started) * 1000

        return HealthCheckResult(
            name=self.name,
            status=HealthStatus.HEALTHY,
            latency_ms=latency,
            details={
                "status_code": response.status_code,
            },
        )
