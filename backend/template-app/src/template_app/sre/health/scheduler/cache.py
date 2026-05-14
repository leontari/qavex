"""
In-memory runtime cache for health scheduler results.

The cache stores the latest plugin execution results refreshed by the
background scheduler loop.

Health HTTP endpoints must read from this cache instead of executing
checks directly during request handling.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.scheduler.state import (
        CachedHealthResult,
    )


class HealthStateCache:
    """Runtime cache for scheduler-managed health results."""

    def __init__(self) -> None:
        """Initialize an empty runtime cache."""
        self._results: dict[str, CachedHealthResult] = {}

    def set(
        self,
        plugin_name: str,
        result: CachedHealthResult,
    ) -> None:
        """
        Store cached plugin result.

        Args:
            plugin_name:
                Plugin identifier.

            result:
                Cached plugin execution result.

        """
        self._results[plugin_name] = result

    def get(
        self,
        plugin_name: str,
    ) -> CachedHealthResult | None:
        """
        Retrieve cached plugin result.

        Args:
            plugin_name:
                Plugin identifier.

        Returns:
            CachedHealthResult | None:
                Cached result if present.

        """
        return self._results.get(plugin_name)

    def snapshot(self) -> dict[str, CachedHealthResult]:
        """
        Return a snapshot of the current runtime cache.

        Returns:
            dict[str, CachedHealthResult]:
                Cached plugin results.

        """
        return dict(self._results)
