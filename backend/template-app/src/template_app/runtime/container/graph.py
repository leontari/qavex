from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import DependencyContract, DependencyScope


@dataclass(slots=True, frozen=True)
class DependencyNode:
    """Dependency graph node."""

    namespace: str
    contract: DependencyContract
    scope: DependencyScope
