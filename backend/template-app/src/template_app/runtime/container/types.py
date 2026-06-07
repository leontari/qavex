"""Lifetime di scopes."""

from __future__ import annotations

from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifetime."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"
    ASYNC = "async"  # TODO: check this


class DependencyVisibility(StrEnum):
    """Dependency visibility."""

    PUBLIC = "public"  # available to all
    PRIVATE = "private"  # available only for namespace members
    KERNEL = (
        "kernel"  # available only within kernel namespace # TODO: check this
    )
