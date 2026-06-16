"""Runtime scopes management."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from template_app.runtime.container.exceptions import (
    ScopeNotFoundError,
)
from template_app.runtime.container.models.scope import (
    ScopeID,
    ScopeSnapshot,
    ScopeState,
)
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

    def create_scope(
        self,
        *,
        owner_id: str | None = None,
        parent_scope: ScopeID | None = None,
    ) -> ScopeID:
        """
        Create runtime scope.

        Returns:
            ScopeID: created scope identifier

        """
        scope_id = ScopeID.new()

        self._scopes[scope_id] = ScopeContext(
            id=scope_id,
            owner_id=owner_id,
            parent_scope=parent_scope,
        )

        return scope_id

    def close_scope(self, scope_id: ScopeID) -> None:
        """
        Destroy scope.

        Cancels all pending initialization futures.
        """
        scope = self.get_scope(scope_id)

        scope.state = ScopeState.CLOSING

        try:
            for future in scope.iter_futures():
                if not future.done():
                    future.cancel()

            scope.clear()

        finally:
            scope.state = ScopeState.CLOSED
            self._scopes.pop(scope_id, None)

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
            raise ScopeNotFoundError(scope_id) from error

    def close_owner_scopes(
        self,
        owner_id: str,
    ) -> None:
        """
        Destroy all scopes owned by owner.

        Args:
            owner_id:
                Runtime owner identifier.

        """
        to_close = [
            scope.id
            for scope in self._scopes.values()
            if scope.owner_id == owner_id
        ]
        for scope_id in to_close:
            self.close_scope(scope_id)

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

    @property
    def snapshots(self) -> tuple[ScopeSnapshot, ...]:
        """
        Create immutable diagnostics snapshots.

        Returns:
            Current scope snapshots.

        """
        return tuple(
            ScopeSnapshot(
                id=scope.id,
                state=scope.state,
                instances=scope.count,
                futures=scope.future_count,
                owner_id=scope.owner_id,
                parent_scope=scope.parent_scope,
            )
            for scope in self._scopes.values()
        )
