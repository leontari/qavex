"""Runtime diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.container.diagnostics.snapshot import (
    ContainerSnapshot,
    GraphSnapshot,
    NamespaceSnapshot,
    RegistrationSnapshot,
    RuntimeSnapshot,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.runtime.manager import (
        DependencyManager,
    )


@dataclass(frozen=True, slots=True)
class ContainerDiagnostics:
    """
    Read-only diagnostics facade.

    It never participates in dependency resolution.

    Diagnostics data is collected from runtime sources:
    - DependencyRegistry
    - ScopeManager
    - SingletonCache
    - RuntimeGraph

    RuntimeGraph represents dependency resolution history
    and must not be treated as the current state of the container.

    Current container state is derived from:

    - DependencyRegistry
    - ScopeManager
    - SingletonCache

    """

    _manager: DependencyManager

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

    @property
    def snapshot(self) -> ContainerSnapshot:
        return ContainerSnapshot(
            registered_dependencies=len(
                self._manager._registry.dependency_ids
            ),
            active_scopes=self._manager._scopes.scopes_count,
            scoped_instances=len(self._manager.singletons),
            resolved_edges=len(self._manager.graph.nodes),
            namespaces=self._manager._registry.namespaces,
        )

    def registrations(self) -> RegistrationSnapshot: ...

    def runtime(self) -> RuntimeSnapshot: ...

    def graph(self) -> GraphSnapshot: ...

    def namespace(self, namespace: Namespace) -> NamespaceSnapshot: ...

    def validate(self): ...
