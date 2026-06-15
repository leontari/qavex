"""Runtime scopes management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import (
    ScopeNotFoundError,
)
from template_app.runtime.container.models.scope import ScopeContext, ScopeID

if TYPE_CHECKING:
    from asyncio import Future

    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True)
class ScopeManager:
    """
    Scope lifecycle manager.

    Source of truth for scoped instances

    Owns all active scopes.
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
        """Destroy scope."""
        scope = self._scopes.pop(scope_id)

        if scope is not None:
            scope.clear()

        # cleanup futures
        to_remove = [k for k in self._scopes_futures if k[0] == scope_id]
        for k in to_remove:
            future = self._scopes_futures.pop(k)
            if not future.done():
                future.cancel()

    def get_scope(self, scope_id: ScopeID) -> ScopeContext:
        """
        Get scope by ID.

        Returns:
            requested scope by ID

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

    @property
    def scopes_count(self) -> int:
        """
        Existing scopes quantity.

        Returns:
            registered scopes quantity

        """
        return len(self._scopes)

    ###########
    # TODO: check later whether it's necessary
    ##########

    def contains(self, scope_id: ScopeID, dependency_id: DependencyID) -> bool:
        return self.get_scope(scope_id).contains(dependency_id)

    def get(self, scope_id: ScopeID, dependency_id: DependencyID) -> object:
        return self.get_scope(scope_id).get(dependency_id)

    def set(
        self,
        scope_id: ScopeID,
        dependency_id: DependencyID,
        instance: object,
    ) -> None:

        self.get_scope(scope_id).set(dependency_id, instance)

    def get_future(
        self,
        scope_id: ScopeID,
        dependency_id: DependencyID,
    ) -> Future[object] | None:

        scope = self.get_scope(scope_id)

        return scope._futures.get(
            dependency_id
        )  # TODO: check api here or there

    def set_future(
        self,
        scope_id: ScopeID,
        dependency_id: DependencyID,
        future: Future[object],
    ) -> None:

        scope = self.get_scope(scope_id)

        scope._futures[dependency_id] = future

    def remove_future(
        self,
        scope_id: ScopeID,
        dependency_id: DependencyID,
    ) -> None:

        scope = self.get_scope(scope_id)

        scope.futures.pop(
            dependency_id,
            None,
        )
