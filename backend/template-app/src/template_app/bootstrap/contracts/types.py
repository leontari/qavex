from __future__ import annotations

from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifetime."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
