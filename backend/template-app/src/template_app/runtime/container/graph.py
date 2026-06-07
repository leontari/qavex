"""Runtime dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from itertools import starmap

if TYPE_CHECKING:
    from template_app.runtime.container.scope import ScopeID


@dataclass(slots=True, frozen=True)
class DependencyNode:
    """Dependency graph node."""

    namespace: str
    contract: str
    provider: str
    scope: str
    visibility: str


@dataclass(slots=True, frozen=True)
class DependencyEdge:
    """Runtime dependency relation."""

    source: str
    target: str


@dataclass(slots=True)
class DependencyGraph:
    """Runtime dependency graph."""

    _nodes: dict[str, DependencyNode] = field(
        default_factory=dict,
    )
    _edges: set[tuple[str, str]] = field(
        default_factory=set,
    )

    # active_scopes: dict[ScopeID, str]

    def add_node(self, node_id: str, node: DependencyNode) -> None:
        self._nodes[node_id] = node

    def add_edge(self, source: str, target: str) -> None:
        self._edges.add((source, target))

    @property
    def nodes(self) -> tuple[DependencyNode, ...]:
        return tuple(self._nodes.values())

    @property
    def edges(self) -> tuple[DependencyEdge, ...]:
        return tuple(starmap(DependencyEdge, sorted(self._edges)))
