"""Scope context manager."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contextvars import Token

    from ..resolution import ResolutionContext, ResolutionManager
    from .manager import ScopeManager
    from .scope import ScopeID


class ScopeHandle:
    """
    Async public scope lifecycle helper.

    Creates and destroys runtime scope automatically.

    Examples:
        async with container.scope():
            ...

    """

    def __init__(
        self,
        scopes: ScopeManager,
        context: ResolutionManager,
    ) -> None:
        self._scopes = scopes
        self._context = context

        self._scope_id: ScopeID | None = None
        self._token: Token[ResolutionContext] | None = None

    async def __aenter__(self) -> ScopeID:
        self._scope_id = self._scopes.create_scope()
        self._token = self._context.enter_scope(self._scope_id)

        return self._scope_id

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._scope_id is not None
        assert self._token is not None

        try:
            self._context.leave_scope(self._token)
        finally:
            self._scopes.close_scope(self._scope_id)
