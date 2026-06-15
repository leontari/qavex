"""Dependency resolution context manager."""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import DependencyCycleError
from template_app.runtime.container.runtime.helpers.context import (
    ResolutionContext,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID
    from template_app.runtime.container.models.scope import ScopeID


@dataclass(slots=True)
class ResolutionContextManager:
    """
    Async-safe local runtime context manager.

    Source of truth for runtime context

    Used for:
        - cycle detection
        - parent dependency tracking
        - graph edge construction
    """

    def __init__(self) -> None:
        self._context: ContextVar[ResolutionContext] = ContextVar(
            "resolution_context",
            default=ResolutionContext(),
        )

    @property
    def current(self) -> ResolutionContext:
        return self._context.get()

    def enter_scope(self, scope_id: ScopeID) -> Token[ResolutionContext]:
        context = self.current

        return self._context.set(
            ResolutionContext(
                scope_id=scope_id,
                plugin_id=context.plugin_id,
                actor_id=context.actor_id,
                request_id=context.request_id,
                stack=context.stack,
            )
        )

    def leave_scope(self, token: Token[ResolutionContext]) -> None:
        self._context.reset(token)

    def enter_resolution(self, dependency_id: DependencyID) -> Token:
        context = self.current

        if dependency_id in context.stack:
            chain = " -> ".join(
                str(item) for item in (*context.stack, dependency_id)
            )
            raise DependencyCycleError(chain)

        return self._context.set(context.push(dependency_id))

    def leave_resolution(self, token: Token[ResolutionContext]) -> None:
        self._context.reset(token)
