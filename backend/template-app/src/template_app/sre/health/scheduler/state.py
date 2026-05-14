"""
Runtime state models for the health scheduler.

This module defines cached runtime scheduler state used by:

- readiness endpoints
- liveness endpoints
- startup probes
- observability pipelines
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from template_app.health.plugins.base import (
    HealthCheckResult,
)


@dataclass(slots=True)
class CachedHealthResult:
    """
    Cached plugin execution result.

    Attributes:
        result:
            Last plugin execution result.

        updated_at:
            Timestamp of cache refresh.

        expires_at:
            Cache expiration timestamp.

    """

    result: HealthCheckResult

    updated_at: datetime

    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        """
        Determine whether the cached result has expired.

        Returns:
            bool:
                True if cache entry is expired.

        """
        return datetime.now(UTC) >= self.expires_at
