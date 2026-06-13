"""Dependency resolution stack."""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True)
class ResolutionContext:
    """
    Async-safe dependency resolution stack.

    Used for:
        - cycle detection
        - parent dependency tracking
        - graph edge construction
    """

    _stack: ContextVar[tuple[DependencyID, ...]] = ContextVar(
        "resolution_stack",
        default=(),
    )

    def enter_resolution(self, dependency_id: DependencyID) -> Token: ...

    def leave_resolution(self, token: Token) -> None: ...

    @property
    def current(self) -> tuple[DependencyID, ...]:
        return self._stack.get()
