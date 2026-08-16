"""Runtime scopes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ScopeID:
    """Unique scope identifier."""

    value: UUID

    @classmethod
    def new(cls) -> ScopeID:
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)


class ScopeState(Enum):
    """
    Runtime scope lifecycle state.

    ACTIVE:
        Scope accepts dependency resolution.
    CLOSING:
        Scope is being destroyed.
    CLOSED:
        Scope is already destroyed.

    """

    ACTIVE = auto()
    CLOSING = auto()
    CLOSED = auto()


@dataclass(frozen=True, slots=True)
class ScopeSnapshot:
    """Immutable scope diagnostics snapshot."""

    id: ScopeID
    state: ScopeState
    instances: int
    futures: int
    owner_id: str | None
    parent_scope: ScopeID | None
