"""Runtime diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import DependencyGraph


@dataclass(frozen=True, slots=True)
class ContainerSnapshot:
    """Immutable container snapshot."""

    graph: DependencyGraph

    @property
    def total_edges(self) -> int:
        return sum(len(edges) for edges in self.graph.edges.values())

    @property
    def total_nodes(self) -> int:
        return len(self.graph.nodes)

    @property
    def total_dependencies(self) -> int:
        return self.total_edges

    @property
    def namespaces(self) -> tuple[str, ...]:
        return tuple(
            sorted({node.namespace.name for node in self.graph.nodes.values()})
        )

    @property
    def scopes(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    edge.scope_id
                    for edge in self.graph.edges
                    if edge.scope_id is not None
                },
            ),
        )
