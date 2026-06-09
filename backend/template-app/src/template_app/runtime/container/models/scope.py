"""Runtime scopes."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(frozen=True, slots=True)
class ScopeID:
    """Unique scope identifier."""

    value: UUID

    @classmethod
    def new(cls) -> ScopeID:
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)


class DependencyScope(StrEnum):
    """Dependency lifetime policy."""

    SINGLETON = "singleton"  # single object for the whole app
    TRANSIENT = "transient"  # new object every time when called
    SCOPED = "scoped"  # single object for a pipeline, then destroy


@dataclass(slots=True)
class ScopeContext:
    """
    Runtime dependency scope.

    Stores scoped instances only.
    """

    id: ScopeID

    _instances: dict[DependencyID:object] = field(default_factory=dict)

    def contains(self, key: DependencyID) -> bool:
        return key in self._instances

    def get(self, key: DependencyID) -> object:
        return self._instances[key]

    def set(self, key: DependencyID, instance: object) -> None:
        self._instances[key] = instance

    def clear(self) -> None:
        self._instances.clear()

    @property
    def instance_count(self) -> int:
        return len(self._instances)


class ScopeState: ...
