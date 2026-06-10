"""DI container contracts."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Protocol,
    TypeVar,
    runtime_checkable,
)

if TYPE_CHECKING:
    from template_app.runtime.container.container import Container

T = TypeVar("T")


@runtime_checkable
class DependencyProvider(Protocol[T]):
    """Dependency provider contract."""

    async def provide(self, resolver: Container) -> T:
        """
        Provide dependency instance.

        Returns:
            Dependency instance.

        """
