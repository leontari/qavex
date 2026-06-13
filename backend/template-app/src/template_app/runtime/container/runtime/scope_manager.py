"""Runtime scopes management."""

from __future__ import annotations

from dataclasses import dataclass, field

from template_app.runtime.container.exceptions import ScopeRequiredError
from template_app.runtime.container.models.scope import ScopeContext, ScopeID


class ScopeHandle:
    def __init__(self, manager: ScopeManager) -> None:
        self._manager = manager
        self._scope_id: ScopeID | None = None

    def __aenter__(self) -> ScopeID:
        self._scope_id = self._manager.create_scope()
        return self._scope_id

    def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._scope_id is not None

        self._manager.close_scope(self._scope_id)


@dataclass(slots=True)
class ScopeManager:
    """
    Scope lifecycle manager.

    Owns all active scopes.
    Scope lifecycle is controlled only here.
    ScopeContext must never be created directly.
    """

    _scopes: dict[ScopeID:ScopeContext] = field(default_factory=dict)

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

    def get_scope(self, scope_id: ScopeID) -> ScopeContext:
        """
        Get scope by ID.

        Returns:
            requested scope by ID

        Raises:
            ScopeRequiredError: if scope_id is not found

        """
        try:
            return self._scopes[scope_id]
        except KeyError as error:
            msg = f"Unknown scope: {scope_id}"
            raise ScopeRequiredError(msg) from error

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
