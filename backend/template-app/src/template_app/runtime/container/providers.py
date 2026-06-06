"""DI container providers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from .types import DependencyScope

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .manager import DependencyManager

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class SingletonProvider(Generic[T]):
    """Singleton provider."""

    factory: Callable[[DependencyManager], T]

    scope: DependencyScope = DependencyScope.SINGLETON

    def provide(self, manager: DependencyManager) -> T:
        """
        Create instance.

        Returns:
            Singleton instance.

        """
        return self.factory(manager)


@dataclass(slots=True, frozen=True)
class FactoryProvider(Generic[T]):
    """Transient provider."""

    factory: Callable[[DependencyManager], T]

    scope: DependencyScope = DependencyScope.TRANSIENT

    def provide(self, manager: DependencyManager) -> T:
        """
        Create new instance.

        Returns:
            New dependency instance.

        """
        return self.factory(manager)


@dataclass(slots=True, frozen=True)
class ScopedProvider(Generic[T]):
    """Scoped provider."""

    factory: Callable[[DependencyManager], T]

    scope: DependencyScope = DependencyScope.SCOPED

    def provide(self, manager: DependencyManager) -> T:
        """
        Create scoped instance.

        Returns:
            Scoped instance.

        """
        return self.factory(manager)


@dataclass(slots=True, frozen=True)
class AsyncProvider(Generic[T]):
    """Async provider."""

    factory: Callable[[DependencyManager], Awaitable[T]]

    scope: DependencyScope = DependencyScope.ASYNC

    async def provide(self, manager: DependencyManager) -> T:
        """
        Create async instance.

        Returns:
            async instance.

        """
        return await self.factory(manager)
