"""
Dependency graph orchestration for health plugins.

This module provides dependency-aware execution ordering for health checks.

The dependency graph prevents:

- redundant checks
- cascading failures
- invalid readiness states
- execution order violations

Execution order is resolved using topological sorting.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.plugins.registry import (
        HealthPluginRegistry,
    )


class HealthDependencyGraph:
    """Dependency graph resolver for health plugins."""

    def __init__(
        self,
        registry: HealthPluginRegistry,
    ) -> None:
        """
        Initialize the dependency graph.

        Args:
            registry:
                Registered health plugins.

        """
        self.registry = registry

    def resolve_execution_order(self) -> list[str]:
        """
        Resolve dependency-aware execution order.

        Returns:
            list[str]:
                Plugin names sorted in execution order.

        Raises:
            ValueError:
                If cyclic dependencies are detected.

        """
        graph: dict[str, set[str]] = defaultdict(set)
        indegree: dict[str, int] = defaultdict(int)

        plugins = self.registry.get_all()

        for plugin in plugins:
            graph[plugin.name]

        for plugin in plugins:
            for dependency in plugin.dependencies:
                graph[dependency].add(plugin.name)
                indegree[plugin.name] += 1

        queue = deque(
            plugin.name for plugin in plugins if indegree[plugin.name] == 0
        )

        result: list[str] = []

        while queue:
            node = queue.popleft()

            result.append(node)

            for child in graph[node]:
                indegree[child] -= 1

                if indegree[child] == 0:
                    queue.append(child)

        if len(result) != len(plugins):
            msg = "Cyclic health dependency graph detected."
            raise ValueError(msg)

        return result
