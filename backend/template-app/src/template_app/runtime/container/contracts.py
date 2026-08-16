"""DI container contracts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .type_vars import T

if TYPE_CHECKING:
    from .models import Namespace


class DependencyResolver(Protocol):
    """
    Dependency resolution contract.

    Minimal runtime interface exposed to dependency providers.

    Providers should depend only on this contract
    and must not depend on Container or DependencyManager.
    """

    async def resolve(
        self,
        contract: type[T],
        *,
        namespace: Namespace,
    ) -> T:
        """
        Resolve dependency instance.

        Args:
            contract:
                Dependency contract to resolve.
            namespace:
                Namespace where dependency is registered.
                Container-specific defaults may be applied when omitted.

        Returns:
            Resolved dependency instance.

        Raises:
            DependencyNotFoundError:
                If dependency is not registered.
            ScopeRequiredError:
                If a scoped dependency is resolved without an active scope.
            DependencyCycleError:
                If a circular dependency is detected.

        """


@runtime_checkable
class DependencyProvider(Protocol[T]):
    """
    Dependency provider contract.

    Providers are responsible only for dependency creation.

    Lifecycle management (singleton, scoped, transient) is handled
    by DependencyManager and must not be implemented inside providers.

    """

    async def provide(self, resolver: DependencyResolver) -> T:
        """
        Create or obtain dependency instance.

        Args:
            resolver:
                Runtime dependency resolver used to resolve
                nested dependencies.

        Returns:
            Resolved dependency instance.

        """


@runtime_checkable
class AsyncDisposable(Protocol):
    """Async resource cleanup contract."""

    async def dispose(self) -> None:
        """Release owned resources."""
