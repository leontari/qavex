from __future__ import annotations

from enum import StrEnum


class RuntimeStatus(StrEnum):
    """Global runtime status."""

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"

    RECOVERING = "recovering"
