"""
Cached runtime state for the health scheduler.

This module defines:

- cached health results
- scheduler runtime state
- staleness tracking metadata
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.plugins.base import HealthCheckResult


@dataclass(slots=True)
class CachedHealthResult:
    """
    Cached plugin execution result.

    Attributes:
        result:
            Last successful health result.

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
                True if cache is expired.

        """
        return datetime.now(UTC) >= self.expires_at
