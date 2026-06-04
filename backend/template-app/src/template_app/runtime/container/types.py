"""Lifetime di scopes."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, TypeAlias

DependencyContract: TypeAlias = type[Any]

ContainerKey: TypeAlias = tuple[str, DependencyContract]


class DependencyScope(StrEnum):
    """Dependency lifetime."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
