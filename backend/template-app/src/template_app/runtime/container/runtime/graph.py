"""Observed runtime dependency graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID

_EMPTY_SET = frozenset()


@dataclass(slots=True)
class DependencyGraph:
    """
    Observed runtime dependency graph.

    Stores dependency relations observed during dependency resolution.

    The graph is built lazily by DependencyManager and contains
    only dependencies that have been resolved at least once.

    Notes:
        This graph is append-only until 'clear()' is called.

        The graph represents historical runtime observations and
        is not a source of truth for the current dependency state.

        Dependency registration metadata is stored in Registry.

    Used for:
        - diagnostics
        - runtime dependency tracing
        - graph export
        - visualization

    """

    _nodes: set[DependencyID] = field(
        default_factory=set,
    )

    # source -> targets
    _edges: dict[DependencyID, set[DependencyID]] = field(
        default_factory=dict,
    )
    # target -> sources
    _reverse_edges: dict[DependencyID, set[DependencyID]] = field(
        default_factory=dict,
    )

    def add_node(self, dependency_id: DependencyID) -> None:
        """
        Register dependency node.

        Args:
            dependency_id:
                Dependency identifier.

        """
        self._nodes.add(dependency_id)

    def add_edge(self, source: DependencyID, target: DependencyID) -> None:
        """
        Register observed dependency relation.

        Creates a directed edge:
            source -> target

        Args:
            source:
                Dependency requesting another dependency.
            target:
                Dependency being resolved.

        """
        self._nodes.add(source)
        self._nodes.add(target)

        self._edges.setdefault(source, set()).add(target)
        self._reverse_edges.setdefault(target, set()).add(source)

    def has_node(self, dependency_id: DependencyID) -> bool:
        """
        Whether dependency node exists in graph.

        Returns:
            True if node was observed.

        """
        return dependency_id in self._nodes

    def successors(
        self, dependency_id: DependencyID
    ) -> frozenset[DependencyID]:
        """
        Get direct dependency successors.

        Successors are dependencies requested by the specified dependency.

        Example:
            A -> B -> C

            successors(A) = {B}
            successors(B) = {C}

        Returns:
            Direct successor nodes.

        """
        return frozenset(self._edges.get(dependency_id, _EMPTY_SET))

    def predecessors(
        self, dependency_id: DependencyID
    ) -> frozenset[DependencyID]:
        """
        Get direct dependency predecessors.

        Predecessors are dependencies that requested the specified dependency.

        Example:
            A -> B -> C

            predecessors(B) = {A}
            predecessors(C) = {B}

        Returns:
            Direct predecessor nodes.

        """
        return frozenset(self._reverse_edges.get(dependency_id, _EMPTY_SET))

    def clear(self) -> None:
        """Remove all observed graph data."""
        self._nodes.clear()
        self._edges.clear()
        self._reverse_edges.clear()

    @property
    def node_count(self) -> int:
        """Total observed node count."""
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        """Total observed edge count."""
        return sum(len(edges) for edges in self._edges.values())

    @property
    def nodes(self) -> frozenset[DependencyID]:
        """Immutable graph nodes view."""
        return frozenset(self._nodes)

    @property
    def edges(self) -> MappingProxyType[DependencyID, frozenset[DependencyID]]:
        """
        Immutable forward adjacency view.

        Source -> Targets

        Returns:
            Read-only adjacency mapping.

        """
        return MappingProxyType({
            source: frozenset(targets)
            for source, targets in self._edges.items()
        })

    @property
    def reverse_edges(
        self,
    ) -> MappingProxyType[DependencyID, frozenset[DependencyID]]:
        """
        Immutable reverse adjacency view.

        Target -> Sources

        """
        return MappingProxyType({
            target: frozenset(sources)
            for target, sources in self._reverse_edges.items()
        })
