from __future__ import annotations

from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifecycle scope."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
