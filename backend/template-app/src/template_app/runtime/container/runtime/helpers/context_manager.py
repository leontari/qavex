"""Dependency resolution context manager."""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import DependencyCycleError
from template_app.runtime.container.runtime.helpers.resolution import (
    ResolutionContext,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID
    from template_app.runtime.container.models.scope import ScopeID


@dataclass(slots=True)
class ResolutionContextManager:
    """
    Resolution context owner.

    Source of truth for current execution context

    Used for:
        - cycle detection
        - parent dependency tracking
        - graph edge construction
    """

    _context: ContextVar[ResolutionContext] = field(
        default_factory=lambda: ContextVar(
            "dependency_resolution_context",
            default=ResolutionContext(),  # TODO: check logic
        ),
    )

    @property
    def current(self) -> ResolutionContext:
        """
        Current execution context.

        Returns:
            Active resolution context.

        """
        return self._context.get()

    @property
    def current_scope(self) -> ScopeID:
        """
        Current active scope.

        Returns:
            Active scope identifier or None.

        """
        return self._context.get().scope_id

    def enter_scope(self, scope_id: ScopeID) -> Token[ResolutionContext]:
        """
        Enter scope context.

        Returns:
            Context token.

        """
        return self._context.set(self.current.with_scope(scope_id=scope_id))

    def leave_scope(self, token: Token[ResolutionContext]) -> None:
        """Leave scope context."""
        self._context.reset(token)

    def enter_resolution(
        self, dependency_id: DependencyID
    ) -> Token[ResolutionContext]:
        """
        Enter dependency resolution.

        Returns:
            Context token.

        Raises:
            DependencyCycleError:
                if dependency cycle is detected.

        """
        context = self.current

        if dependency_id in context.stack:
            chain = " -> ".join(
                str(item) for item in (*context.stack, dependency_id)
            )
            raise DependencyCycleError(chain)

        return self._context.set(context.push(dependency_id))

    def leave_resolution(self, token: Token[ResolutionContext]) -> None:
        """Leave dependency resolution."""
        self._context.reset(token)
