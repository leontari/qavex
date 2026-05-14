"""
In-memory cache for health check results.

This cache stores the latest successful results produced by the
background health scheduler.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.scheduler.state import CachedHealthResult


class HealthStateCache:
    """Runtime cache for health results."""

    def __init__(self) -> None:
        """Initialize an empty health state cache."""
        self._results: dict[str, CachedHealthResult] = {}

    def set(
        self,
        plugin_name: str,
        result: CachedHealthResult,
    ) -> None:
        """
        Store a cached plugin result.

        Args:
            plugin_name:
                Plugin identifier.

            result:
                Cached plugin result.

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
        Return a snapshot of all cached results.

        Returns:
            dict[str, CachedHealthResult]:
                Cached results by plugin name.

        """
        return dict(self._results)
