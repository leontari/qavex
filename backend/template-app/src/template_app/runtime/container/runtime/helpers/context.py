"""Current dependency resolution context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import (
        DependencyID,
    )
    from template_app.runtime.container.models.scope import ScopeID


@dataclass(slots=True, frozen=True)
class ResolutionContext:
    """Current runtime resolution context."""

    scope_id: ScopeID | None = None  # lifetime boundary

    plugin_id: str | None = None  # runtime owner

    actor_id: str | None = None  # execution unit

    request_id: str | None = None  # tracing / diagnostics

    stack: tuple[DependencyID, ...] = field(
        default_factory=tuple,
    )

    def push(
        self,
        dependency_id: DependencyID,
    ) -> ResolutionContext:
        return ResolutionContext(
            scope_id=self.scope_id,
            plugin_id=self.plugin_id,
            actor_id=self.actor_id,
            request_id=self.request_id,
            stack=(*self.stack, dependency_id),
        )

    def pop(self) -> ResolutionContext:
        return ResolutionContext(
            scope_id=self.scope_id,
            plugin_id=self.plugin_id,
            actor_id=self.actor_id,
            request_id=self.request_id,
            stack=self.stack[:-1],
        )
