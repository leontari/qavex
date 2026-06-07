"""DI container contracts."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)

if TYPE_CHECKING:
    from .manager import DependencyManager
    from .types import DependencyScope

T = TypeVar("T")


@runtime_checkable
class DependencyProvider(Protocol[T]):
    """Dependency provider contract."""

    scope: DependencyScope

    def provide(self, manager: DependencyManager) -> T:
        """
        Create dependency instance.

        Returns:
            Dependency instance.

        """


@runtime_checkable
class AsyncDependencyProvider(Protocol[T]):
    """Async dependency provider contract."""

    scope: DependencyScope

    async def provide(self, manager: DependencyManager) -> T:
        """
        Create dependency instance asynchronously.

        Returns:
            Dependency instance.

        """


@runtime_checkable
class PluginDeclaration(Protocol):
    """
    Declarative plugin contract.

    Used by Kernel autodiscovery
    """

    name: str
    namespace: str
    dependencies: tuple[type[Any], ...]
    exports: tuple[type[Any], ...]
