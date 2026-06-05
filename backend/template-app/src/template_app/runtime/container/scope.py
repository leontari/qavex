from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any


@dataclass(frozen=True, slots=True)
class ScopeID:
    value: UUID

    @classmethod
    def new(cls) -> "ScopeID":
        return cls(uuid4())


@dataclass(slots=True)
class ScopeContext:
    """Runtime scope."""

    _id: ScopeID = field(
        default_factory=ScopeID.new,
    )

    _instances: dict[type[Any], object] = field(
        default_factory=dict,
    )

    def contains(self, contract: type[Any]) -> bool:
        return contract in self._instances

    def get(self, contract: type[Any]) -> object:
        return self._instances[contract]

    def set(self, contract: type[Any], instance: object) -> None:
        self._instances[contract] = instance

    def clear(self) -> None:
        self._instances.clear()
