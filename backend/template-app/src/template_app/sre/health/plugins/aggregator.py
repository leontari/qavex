"""
Health result aggregation logic.

This module provides aggregation strategies used to compute overall
runtime health states from individual plugin results.

Aggregation is dependency-aware and supports degraded runtime states.
"""

from __future__ import annotations

import time

from template_app.health.plugins.base import (
    HealthCheckResult,
    HealthStatus,
)
from template_app.health.plugins.results import (
    AggregatedHealthResult,
)


class HealthAggregator:
    """Aggregate plugin health results into a single runtime state."""

    def aggregate(
        self,
        results: list[HealthCheckResult],
    ) -> AggregatedHealthResult:
        """
        Aggregate plugin results.

        Aggregation rules:

        - any UNHEALTHY critical dependency -> UNHEALTHY
        - any DEGRADED dependency -> DEGRADED
        - otherwise -> HEALTHY

        Args:
            results:
                Plugin execution results.

        Returns:
            AggregatedHealthResult:
                Aggregated runtime health result.

        """
        overall = HealthStatus.HEALTHY

        for result in results:
            if result.status == HealthStatus.UNHEALTHY:
                overall = HealthStatus.UNHEALTHY
                break

            if result.status == HealthStatus.DEGRADED:
                overall = HealthStatus.DEGRADED

        return AggregatedHealthResult(
            status=overall,
            checks=results,
            generated_at=time.time(),
        )
