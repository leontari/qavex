"""Current dependency resolution context."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import (
        DependencyID,
    )
    from template_app.runtime.container.models.scope import ScopeID


@dataclass(slots=True, frozen=True)
class ResolutionContext:
    """
    Current dependency resolution state.

    Lives inside ContextVar.

    Stores:
        - active scope
        - dependency resolution stack

    Used for:
        - cycle detection
        - graph construction
        - scoped resolution

    """

    scope_id: ScopeID | None = None
    stack: tuple[DependencyID, ...] = field(default_factory=tuple)

    def push(self, dependency_id: DependencyID) -> ResolutionContext:
        """
        Append dependency to resolution stack.

        Returns:
            Updated resolution context.

        """
        return replace(self, stack=(*self.stack, dependency_id))

    def pop(self) -> ResolutionContext:
        """
        Remove last dependency from resolution stack.

        Returns:
            Updated resolution context.

        """
        return replace(self, stack=self.stack[:-1])
