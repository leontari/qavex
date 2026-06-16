"""Runtime scopes management."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from template_app.runtime.container.exceptions import (
    ScopeNotFoundError,
)
from template_app.runtime.container.models.scope import ScopeID
from template_app.runtime.container.runtime.helpers.context import ScopeContext


@dataclass(slots=True)
class ScopeManager:
    """
    Scope lifecycle manager.

    Source of truth for scoped instances.
    Stores all active scopes.

    Scope lifecycle is controlled only here.
    ScopeContext must never be created directly.
    """

    _scopes: dict[ScopeID, ScopeContext] = field(default_factory=dict)

    def create_scope(self) -> ScopeID:
        """
        Create runtime scope.

        Returns:
            ScopeID: created scope identifier

        """
        scope_id = ScopeID.new()

        self._scopes[scope_id] = ScopeContext(id=scope_id)

        return scope_id

    def close_scope(self, scope_id: ScopeID) -> None:
        """
        Destroy scope.

        Cancels all pending initialization futures.
        """
        scope = self._scopes.pop(scope_id)

        for future in scope.iter_futures():
            if not future.done():
                future.cancel()

        scope.clear()

    def get_scope(self, scope_id: ScopeID) -> ScopeContext:
        """
        Get scope by ID.

        Returns:
            requested scope

        Raises:
            ScopeNotFoundError: if scope_id is not found

        """
        try:
            return self._scopes[scope_id]
        except KeyError as error:
            msg = f"Unknown scope: {scope_id}"
            raise ScopeNotFoundError(msg) from error

    def exists(self, scope_id: ScopeID) -> bool:
        """
        Whether scope exists.

        Returns:
            True if scope exists.

        """
        return scope_id in self._scopes

    #############
    # Diagnostics
    #############
    @property
    def scopes_count(self) -> int:
        """
        Existing scopes quantity.

        Returns:
            registered scopes quantity

        """
        return len(self._scopes)

    @property
    def active_scopes(self) -> frozenset[ScopeID]:
        """
        Active scope identifiers.

        Returns:
            Immutable collection of active scope IDs.

        """
        return frozenset(self._scopes)

    @property
    def scope_contexts(self) -> MappingProxyType[ScopeID, ScopeContext]:
        """
        Active scope contexts.

        Intended for diagnostics only.

        Returns:
            Read-only mapping of active scopes.

        """
        return MappingProxyType(self._scopes)
