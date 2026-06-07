from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any


@dataclass(frozen=True, slots=True)
class ScopeID:
    value: UUID

    @classmethod
    def new(cls) -> "ScopeID":
        return ScopeID(uuid4())


@dataclass(slots=True)
class ScopeContext:
    """Runtime scope."""

    _id: ScopeID = field(default_factory=ScopeID.new)
    _instances: dict[tuple[type[Any], ScopeID], object] = field(
        default_factory=dict
    )

    @property
    def id(self) -> ScopeID:
        return self._id

    def contains(self, contract: type[Any]) -> bool:
        return (contract, self._id) in self._instances

    def get(self, contract: type[Any]) -> object:
        return self._instances[contract, self._id]

    def set(self, contract: type[Any], instance: object) -> None:
        self._instances[contract, self._id] = instance

    def clear(self) -> None:
        self._instances.clear()
