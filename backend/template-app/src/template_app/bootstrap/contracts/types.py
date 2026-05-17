from __future__ import annotations

from enum import Enum


class DependencyScope(str, Enum):
    """Dependency lifetime."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
