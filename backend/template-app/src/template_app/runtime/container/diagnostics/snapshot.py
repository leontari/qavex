from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID
    from template_app.runtime.container.models.namespace import Namespace


@dataclass(frozen=True, slots=True)
class ContainerSnapshot:
    registered_dependencies: int
    namespaces: tuple[str, ...]
    singleton_instances: int
    active_scopes: int
    graph: GraphSnapshot
    scoped_instances: int
    resolved_nodes: int
    resolved_edges: int


@dataclass(frozen=True, slots=True)
class RegistrationSnapshot: ...


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot: ...


@dataclass(frozen=True, slots=True)
class GraphSnapshot:
    nodes: frozenset[DependencyID]
    edges: dict[DependencyID, frozenset[DependencyID]]


@dataclass(frozen=True, slots=True)
class NamespaceSnapshot:
    namespace: Namespace
    dependencies: int
    singletons: int
    scoped: int
