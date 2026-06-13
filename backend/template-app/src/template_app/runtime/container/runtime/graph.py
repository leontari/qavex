"""Runtime dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True)
class DependencyGraph:
    """
    Runtime dependency graph.

    Built dynamically during DependencyManager.resolve().

    RuntimeGraph stores resolution history.
    RuntimeGraph is not a source of truth for current dependency state.

    Used for:
        - diagnostics
        - runtime dependency tracing
        - graph export
        - visualization

    """

    _nodes: set[DependencyID] = field(
        default_factory=set,
    )
    _edges: dict[DependencyID, set[DependencyID]] = field(
        default_factory=dict,
    )

    def add_node(self, key: DependencyID) -> None:
        """Register isolated node."""
        self._nodes.add(key)

    def add_edge(self, source: DependencyID, target: DependencyID) -> None:
        """
        Register dependency edge.

        Source -> Target.

        """
        self._nodes.add(source)
        self._nodes.add(target)

        self._edges.setdefault(source, set()).add(target)

    def contains(self, dependency_id: DependencyID) -> bool:
        return dependency_id in self._nodes

    def successors(
        self, dependency_id: DependencyID
    ) -> frozenset[DependencyID]:
        return frozenset(self._edges.get(dependency_id, ()))

    def clear(self) -> None:
        self._nodes.clear()
        self._edges.clear()

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_cont(self) -> int:
        return sum(len(edges) for edges in self._edges.values())

    @property
    def nodes(self) -> frozenset[DependencyID]:
        return frozenset(self._nodes)

    @property
    def edges(self) -> dict[DependencyID, frozenset[DependencyID]]:
        return {node: frozenset(edges) for node, edges in self._edges.items()}
