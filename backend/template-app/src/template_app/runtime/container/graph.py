from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DependencyNode:
    """Dependency graph node."""

    namespace: str
    contract: str
    provider: str
    scope: str
    visibility: str


@dataclass(slots=True, frozen=True)
class DependencyGraph:
    """Dependency graph snapshot."""

    nodes: tuple[DependencyNode, ...]
