"""DI provider factory."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from template_app.runtime.container.models.scope import DependencyScope
    from template_app.runtime.container.runtime.manager import (
        DependencyManager,
    )

T = TypeVar("T")

Factory = Callable[["DependencyManager"], T | Awaitable[T]]


@dataclass(slots=True, frozen=True)
class Provider(Generic[T]):
    """Universal dependency provider factory."""

    factory: Factory[T]
    scope: DependencyScope

    async def provide(self, manager: DependencyManager) -> T:
        """
        Provide dependency object.

        Returns:
            Resolved dependency object

        """
        resolved = self.factory(manager)

        if hasattr(resolved, "__await__"):
            resolved = await resolved

        return resolved
