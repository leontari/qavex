"""
Runtime lifecycle registry.

This module provides centralized registration and access to runtime-managed
resources such as:

- database engines
- Redis clients
- Kafka producers
- schedulers
- HTTP clients
- background task managers

The registry acts as the application's runtime dependency container.
"""

from __future__ import annotations

from typing import Any


class LifecycleRegistry:
    """Runtime resource registry."""

    def __init__(self) -> None:
        """Initialize an empty lifecycle registry."""
        self._resources: dict[str, Any] = {}

    def register(
        self,
        name: str,
        resource: Any,
    ) -> None:
        """
        Register a runtime resource.

        Args:
            name:
                Resource identifier.

            resource:
                Runtime-managed resource.

        """
        self._resources[name] = resource

    def get(
        self,
        name: str,
    ) -> Any:
        """
        Retrieve a runtime resource.

        Args:
            name:
                Resource identifier.

        Returns:
            Any:
                Registered runtime resource.

        """
        return self._resources[name]

    def all(self) -> dict[str, Any]:
        """
        Return all registered resources.

        Returns:
            dict[str, Any]:
                Registered runtime resources.

        """
        return dict(self._resources)
