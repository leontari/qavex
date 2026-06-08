"""Container runtime types."""

from __future__ import annotations

from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifetime policy."""

    SINGLETON = "singleton"  # single object for the whole app
    TRANSIENT = "transient"  # new object every time when called
    SCOPED = "scoped"  # single object for a pipeline, then destroy


class DependencyVisibility(StrEnum):
    """Dependency visibility policy."""

    PUBLIC = "public"  # available to all
    PRIVATE = "private"  # available only for namespace members
