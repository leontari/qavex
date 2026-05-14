"""
Kafka health provider.

This module defines a runtime health plugin for validating Kafka broker
availability and metadata responsiveness.
"""

from __future__ import annotations

import time

from aiokafka import AIOKafkaProducer

from template_app.health.plugins.base import (
    HealthCheckPlugin,
    HealthCheckResult,
    HealthStatus,
    RefreshPolicy,
)


class KafkaHealthPlugin(HealthCheckPlugin):
    """Kafka runtime health plugin."""

    name = "kafka"

    policy = RefreshPolicy(
        interval_seconds=10,
        timeout_seconds=5,
        critical=True,
        cache_ttl_seconds=15,
    )

    def __init__(
        self,
        producer: AIOKafkaProducer,
    ) -> None:
        """
        Initialize the Kafka health plugin.

        Args:
            producer:
                Async Kafka producer instance.
        """
        self.producer = producer

    async def check(self) -> HealthCheckResult:
        """
        Validate Kafka broker availability.

        Returns:
            HealthCheckResult:
                Kafka health result.
        """
        started = time.perf_counter()

        try:
            await self.producer.client.bootstrap()

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
