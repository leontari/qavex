"""Dependency resolution context manager."""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass, field, replace
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
    Dependency resolution context manager.

    Owns current ContextVar state.

    Source of truth for:
        - active scope
        - dependency resolution stack

    """

    _context: ContextVar[ResolutionContext | None] = field(
        default_factory=lambda: ContextVar(
            "resolution_context",
            default=None,
        ),
    )

    @property
    def current_context(self) -> ResolutionContext:
        """
        Current resolution context.

        Returns:
            Current context snapshot.

        """
        context = self._context.get()

        if context is None:
            return ResolutionContext()

        return context

    #################
    # Scope lifecycle
    #################

    def enter_scope(self, scope_id: ScopeID) -> Token[ResolutionContext]:
        """
        Activate scope.

        Returns:
            Context token.

        """
        current_context = self.current_context
        updated_context = replace(current_context, scope_id=scope_id)

        return self._context.set(updated_context)

    def leave_scope(self, token: Token[ResolutionContext]) -> None:
        """Restore previous scope state."""
        self._context.reset(token)

    ######################
    # Resolution lifecycle
    ######################

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
        current_context = self.current_context

        if dependency_id in current_context.stack:
            raise DependencyCycleError(current_context.stack, dependency_id)

        return self._context.set(current_context.push(dependency_id))

    def leave_resolution(self, token: Token[ResolutionContext]) -> None:
        """Leave dependency resolution."""
        self._context.reset(token)
