"""Runtime dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.container.namespace import Namespace


@dataclass(slots=True, frozen=True)
class DependencyNode:
    """Dependency graph node."""

    contract: type[Any]
    namespace: Namespace


@dataclass(slots=True)
class DependencyGraph:
    """
    Runtime dependency graph.

    Built dynamically during resolve().

    Stores:
        contract -> dependencies

    Used for:
        - validation
        - cycle detection
        - diagnostics
        - visualization
    """

    _nodes: dict[str, DependencyNode] = field(default_factory=dict)
    _edges: dict[str, set[str]] = field(default_factory=dict)

    def add_node(self, node_id: str, node: DependencyNode) -> None:
        """Register isolated node."""
        self._nodes[node_id] = node

    def add_edge(self, source: str, target: str) -> None:
        """
        Register dependency edge.

        Source -> Target.

        """
        self._nodes.add(source)
        self._nodes.add(target)

        self._edges.setdefault(source, set()).add(target)

    @property
    def nodes(self) -> frozenset[str]:
        return frozenset(self._nodes)

    @property
    def edges(self) -> dict[str, set[str]]:
        return self._edges

    def validate(self) -> None:
        """
        Validate graph.

        Detect dependency cycles.

        """
        visited: set[str] = set()
        stack: set[str] = set()

        def dfs(node: str) -> None:
            if node in stack:
                msg = f"Dependency cycle detected at '{node}'"
                raise RuntimeError(msg)

            if node in visited:
                return

            stack.add(node)

            for dependency in self._edges.get(node, ()):
                dfs(dependency)

            stack.remove(node)
            visited.add(node)

        for node in self._edges:
            dfs(node)
