"""Runtime scope management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from .exceptions import ScopeRequiredError


@dataclass(frozen=True, slots=True)
class ScopeID:
    value: UUID

    @classmethod
    def new(cls) -> ScopeID:
        return cls(uuid4())


@dataclass(slots=True)
class ScopeContext:
    """Runtime scope state."""

    # _id: ScopeID = field(default_factory=ScopeID.new)

    # _instances: dict[tuple[type[Any], ScopeID], object] = field(
    #     default_factory=dict
    # )

    id: ScopeID

    _instances: dict[type[Any], object] = field(
        default_factory=dict,
    )

    # def contains(self, contract: type[Any]) -> bool:
    #     return (contract, self._id) in self._instances

    def contains(self, contract: type[Any]) -> bool:
        return contract in self._instances

    # def get(self, contract: type[Any]) -> object:
    #     return self._instances[contract, self._id]

    def get(self, contract: type[Any]) -> object:
        return self._instances[contract]

    # def set(self, contract: type[Any], instance: object) -> None:
    #     self._instances[contract, self._id] = instance

    def set(self, contract: type[Any], instance: object) -> None:
        self._instances[contract] = instance

    def clear(self) -> None:
        self._instances.clear()  # TODO: check this


@dataclass(slots=True)
class ScopeManager:
    """Owns all runtime scopes."""

    _scopes: dict[UUID, ScopeContext] = field(
        default_factory=dict,
    )

    def create_scope(self) -> ScopeID:
        scope_id = ScopeID.new()

        self._scopes[scope_id.value] = ScopeContext(id=scope_id)

        return scope_id

    def get_scope(self, scope_id: ScopeID) -> ScopeContext:
        try:
            return self._scopes[scope_id.value]
        except KeyError as error:
            msg = f"Unknown scope: {scope_id.value}"
            raise ScopeRequiredError(msg) from error

    def close_scope(self, scope_id: ScopeID) -> None:
        self._scopes.pop(scope_id.value, None)
