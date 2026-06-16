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
    Current execution context.

    Stored inside ContextVar.

    Used for:
        - cycle detection
        - dependency tracing
        - scope propagation
        - plugin isolation
        - actor isolation
    """

    scope_id: ScopeID | None = None  # lifetime boundary
    plugin_id: str | None = None  # runtime owner
    actor_id: str | None = None  # execution unit
    request_id: str | None = None  # tracing / diagnostics

    stack: tuple[DependencyID, ...] = field(default_factory=tuple)

    def push(self, dependency_id: DependencyID) -> ResolutionContext:
        return replace(self, stack=(*self.stack, dependency_id))

    def pop(self) -> ResolutionContext:
        return replace(self, stack=self.stack[:-1])

    def with_scope(self, scope_id: ScopeID | None) -> ResolutionContext:
        return replace(self, scope_id=scope_id)
