"""
Aggregated health result models.

This module defines high-level aggregated health states used by:

- readiness endpoints
- liveness endpoints
- startup probes
- orchestration dashboards
- observability pipelines
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.plugins.base import (
        HealthCheckResult,
        HealthStatus,
    )


@dataclass(slots=True)
class AggregatedHealthResult:
    """
    Aggregated runtime health result.

    Attributes:
        status:
            Overall aggregated health status.

        checks:
            Individual plugin execution results.

        generated_at:
            Unix timestamp when aggregation completed.

    """

    status: HealthStatus

    checks: list[HealthCheckResult]

    generated_at: float
