"""Kernel di container types."""

from __future__ import annotations

from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifetime policy."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class DependencyVisibility(StrEnum):
    """Dependency visibility policy."""

    PUBLIC = "public"  # available to all
    PRIVATE = "private"  # available only for namespace members
    KERNEL = "kernel"
