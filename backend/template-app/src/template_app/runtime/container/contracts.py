"""DI container contracts."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Protocol,
    TypeVar,
    runtime_checkable,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.scope import DependencyScope
    from template_app.runtime.container.runtime.manager import (
        DependencyManager,
    )

T = TypeVar("T")


@runtime_checkable
class DependencyProvider(Protocol[T]):
    """Dependency provider contract."""

    scope: DependencyScope

    async def provide(self, manager: DependencyManager) -> T:
        """
        Create dependency instance.

        Returns:
            Dependency instance.

        """
