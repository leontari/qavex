"""
Central registry of system dependencies.

Dependency registry (enterprise core)
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

HealthCheck = Callable[[], Awaitable[bool]]


class HealthRegistry:
    """Registry of dependency health checks."""

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}

    def register(self, name: str, check: HealthCheck) -> None:
        """
        Register health check.

        Args:
            name:
                Dependency name.

            check:
                Async health check function.
        """
        self._checks[name] = check

    def items(self):
        """
        Return registered health checks.
        """
        return self._checks.items()


registry = HealthRegistry()
