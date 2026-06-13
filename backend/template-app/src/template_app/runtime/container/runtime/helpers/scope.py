"""Scope context manager."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.scope import ScopeID
    from template_app.runtime.container.runtime.scope_manager import (
        ScopeManager,
    )


class ScopeHandle:
    """
    Async scope context manager.

    Creates and destroys runtime scope automatically.

    Examples:
        async with container.scope() as scope_id:
            ...

    """

    def __init__(self, manager: ScopeManager) -> None:
        self._manager = manager
        self._scope_id: ScopeID | None = None

    def __aenter__(self) -> ScopeID:
        self._scope_id = self._manager.create_scope()
        return self._scope_id

    def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._scope_id is not None

        self._manager.close_scope(self._scope_id)
