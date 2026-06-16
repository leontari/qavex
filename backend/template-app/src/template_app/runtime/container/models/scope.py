"""Runtime scopes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from uuid import UUID


class DependencyScope(StrEnum):
    """Dependency lifetime policy."""

    SINGLETON = "singleton"  # single object for the whole app
    TRANSIENT = "transient"  # new object every time when called
    SCOPED = "scoped"  # single object for a pipeline, then destroy


@dataclass(frozen=True, slots=True)
class ScopeID:
    """Unique scope identifier."""

    value: UUID

    @classmethod
    def new(cls) -> ScopeID:
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)
