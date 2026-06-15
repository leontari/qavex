"""Runtime scopes."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from asyncio import Future

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
    Active dependency scope.

    Stores scoped instances only.
    """

    id: ScopeID

    _instances: dict[DependencyID, object] = field(
        default_factory=dict,
    )

    # _futures: dict[tuple[ScopeID, DependencyID], Future] = field(
    #     default_factory=dict,
    # )
    _futures: dict[DependencyID, Future[object]] = field(
        default_factory=dict,
    )

    def contains(self, dependency_id: DependencyID) -> bool:
        return dependency_id in self._instances

    def get(self, dependency_id: DependencyID) -> object:
        return self._instances[dependency_id]

    def set(self, dependency_id: DependencyID, instance: object) -> None:
        self._instances[dependency_id] = instance

    def clear(self) -> None:
        self._instances.clear()
        self._futures.clear()

    @property
    def instance_count(self) -> int:
        return len(self._instances)


class ScopeState: ...
