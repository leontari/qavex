"""Runtime scopes management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from .exceptions import ScopeRequiredError


@dataclass(frozen=True, slots=True)
class ScopeID:
    """Unique scope identifier."""

    value: UUID  # TODO: check this

    @classmethod
    def new(cls) -> ScopeID:
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(slots=True)
class ScopeContext:
    """
    Runtime dependency scope.

    Stores scoped instances only.
    """

    id: ScopeID

    _instances: dict[tuple[str, type[Any]]] = field(default_factory=dict)

    def contains(self, key: tuple[str, type[Any]]) -> bool:
        return key in self._instances

    def get(self, key: tuple[str, type[Any]]) -> object:
        return self._instances[key]

    def set(self, key: tuple[str, type[Any]], instance: object) -> None:
        self._instances[key] = instance

    def clear(self) -> None:
        self._instances.clear()

    @property
    def instance_count(self) -> int:
        return len(self._instances)


@dataclass(slots=True)
class ScopeManager:
    """
    Scope lifecycle manager.

    Owns all active scopes.
    Scope lifecycle is controlled only here.
    ScopeContext must never be created directly.
    """

    _scopes: dict[ScopeID, ScopeContext] = field(default_factory=dict)

    def create_scope(self) -> ScopeContext:
        """Create runtime scope."""
        scope = ScopeContext(id=ScopeID.new())
        self._scopes[scope.id] = scope

        return scope

    def close_scope(self, scope_id: ScopeID) -> None:
        """Destroy scope."""
        scope = self._scopes.pop(scope_id, None)

        if scope is not None:
            scope.clear()

    def get_scope(self, scope_id: ScopeID) -> ScopeContext:
        try:
            return self._scopes[scope_id]
        except KeyError as error:
            msg = f"Unknown scope: {scope_id}"
            raise ScopeRequiredError(msg) from error

    def exists(self, scope_id: ScopeID) -> bool:
        """
        Check whether scope exists.

        Returns:
            True if scope exists.

        """
        return scope_id in self._scopes

    @property
    def scopes_count(self) -> int:
        """Count existing scopes."""
        return len(self._scopes)
