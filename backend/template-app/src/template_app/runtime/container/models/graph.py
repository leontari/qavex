from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True, frozen=True)
class DependencyNode:
    """Dependency graph node."""

    id: DependencyID


@dataclass(slots=True, frozen=True)
class DependencyEdge:
    """Directed dependency relationship."""

    source: DependencyID
    target: DependencyID


@dataclass(slots=True, frozen=True)
class DependencyGraph:
    """Graph internal mapping."""

    nodes: set[DependencyID]
    edges: dict[DependencyID, set[DependencyID]]
