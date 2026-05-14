"""
Health plugin registry.

This module provides a centralized registry for all health plugins
participating in the runtime health orchestration system.

The registry is responsible for:

- plugin registration
- plugin lookup
- dependency graph construction
- scheduler discovery
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.plugins.base import HealthCheckPlugin


class HealthPluginRegistry:
    """
    Registry for health check plugins.

    The registry stores plugin instances indexed by unique plugin names.
    """

    def __init__(self) -> None:
        """Initialize an empty plugin registry."""
        self._plugins: dict[str, HealthCheckPlugin] = {}

    def register(self, plugin: HealthCheckPlugin) -> None:
        """
        Register a health plugin.

        Args:
            plugin:
                Plugin instance to register.

        Raises:
            ValueError:
                If a plugin with the same name already exists.

        """
        if plugin.name in self._plugins:
            msg = f"Plugin already registered: {plugin.name}"
            raise ValueError(msg)

        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> HealthCheckPlugin:
        """
        Retrieve a plugin by name.

        Args:
            name:
                Plugin identifier.

        Returns:
            HealthCheckPlugin:
                Registered plugin instance.

        Raises:
            KeyError:
                If plugin does not exist.

        """
        return self._plugins[name]

    def get_all(self) -> list[HealthCheckPlugin]:
        """
        Return all registered plugins.

        Returns:
            list[HealthCheckPlugin]:
                Registered plugin instances.

        """
        return list(self._plugins.values())
