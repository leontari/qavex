from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import DependencyGraph


@dataclass(frozen=True, slots=True)
class ContainerSnapshot:
    """Immutable container snapshot."""

    _graph: DependencyGraph

    @property
    def total_dependencies(self) -> int:
        return len(self._graph.nodes)

    @property
    def namespaces(self) -> tuple[str, ...]:
        return tuple(sorted({node.namespace for node in self._graph.nodes}))
