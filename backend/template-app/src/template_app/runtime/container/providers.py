"""DI container providers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from .types import DependencyScope

if TYPE_CHECKING:
    from collections.abc import Callable

    from .container import Container

T = TypeVar("T")


@dataclass(slots=True)
class SingletonProvider:
    """Singleton dependency provider."""

    factory: Callable[[Container], T]

    scope: DependencyScope = DependencyScope.SINGLETON

    def provide(self, container: Container) -> T:
        """
        Build dependency.

        Returns:
            Singleton instance.

        """
        return self.factory(container)


@dataclass(slots=True)
class FactoryProvider:
    """Transient dependency provider."""

    factory: Callable[[Container], T]

    scope: DependencyScope = DependencyScope.TRANSIENT

    def provide(self, container: Container) -> T:
        """
        Build dependency.

        Returns:
            New dependency instance.

        """
        return self.factory(container)
