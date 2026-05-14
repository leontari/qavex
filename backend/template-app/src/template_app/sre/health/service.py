"""
High-level health orchestration service.

This module provides the main service layer used by HTTP endpoints,
runtime orchestration, and Kubernetes probes.

The service coordinates:

- scheduler state access
- cached result aggregation
- readiness evaluation
- liveness evaluation
- startup readiness validation
- stale cache detection

The service intentionally avoids executing infrastructure checks
directly during HTTP requests. All runtime state is retrieved from the
background scheduler cache.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from template_app.health.plugins.base import (
    HealthCheckResult,
    HealthStatus,
)

if TYPE_CHECKING:
    from template_app.health.plugins.aggregator import (
        HealthAggregator,
    )
    from template_app.health.plugins.results import (
        AggregatedHealthResult,
    )
    from template_app.health.scheduler.cache import (
        HealthStateCache,
    )
    from template_app.health.scheduler.policies import (
        SchedulerPolicy,
    )


@dataclass(slots=True)
class LivenessResult:
    """
    Liveness probe result.

    Attributes:
        status:
            Runtime liveness status.

        timestamp:
            Probe evaluation timestamp.

    """

    status: HealthStatus

    timestamp: float


class HealthService:
    """
    High-level runtime health orchestration service.

    This service provides:

    - readiness evaluation
    - liveness evaluation
    - startup probe support
    - stale cache detection
    - aggregated runtime state access

    """

    def __init__(
        self,
        cache: HealthStateCache,
        aggregator: HealthAggregator,
        scheduler_policy: SchedulerPolicy,
    ) -> None:
        """
        Initialize the health service.

        Args:
            cache:
                Runtime scheduler cache.

            aggregator:
                Aggregated health result strategy.

            scheduler_policy:
                Scheduler runtime policy.

        """
        self.cache = cache
        self.aggregator = aggregator
        self.scheduler_policy = scheduler_policy

    def get_readiness(self) -> AggregatedHealthResult:
        """
        Compute aggregated readiness state.

        Returns:
            AggregatedHealthResult:
                Aggregated readiness result.

        """
        cached_results = self.cache.snapshot()

        results: list[HealthCheckResult] = []

        for cached in cached_results.values():
            if self._is_stale(cached.updated_at):
                results.append(
                    HealthCheckResult(
                        name=cached.result.name,
                        status=HealthStatus.UNHEALTHY,
                        latency_ms=0.0,
                        error="Health cache is stale.",
                    ),
                )

                continue

            results.append(cached.result)

        return self.aggregator.aggregate(results)

    def get_liveness(self) -> LivenessResult:
        """
        Compute runtime liveness state.

        Liveness intentionally does not validate infrastructure
        dependencies. It only verifies that the runtime orchestration
        system itself is operational.

        Returns:
            LivenessResult:
                Runtime liveness result.

        """
        return LivenessResult(
            status=HealthStatus.HEALTHY,
            timestamp=datetime.now(UTC).timestamp(),
        )

    def is_ready(self) -> bool:
        """
        Determine whether the runtime is fully ready.

        Returns:
            bool:
                True if runtime is ready.

        """
        readiness = self.get_readiness()

        return readiness.status != HealthStatus.UNHEALTHY

    def _is_stale(
        self,
        updated_at: datetime,
    ) -> bool:
        """
        Determine whether cached scheduler state is stale.

        Args:
            updated_at:
                Cache update timestamp.

        Returns:
            bool:
                True if cache entry is stale.

        """
        now = datetime.now(UTC)

        delta_seconds = (now - updated_at).total_seconds()

        return delta_seconds > self.scheduler_policy.stale_after_seconds
