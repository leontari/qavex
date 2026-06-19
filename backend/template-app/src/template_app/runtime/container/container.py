"""Runtime dependency injection container."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .diagnostics import ContainerDiagnostics
from .models import DependencyScope, DependencyVisibility
from .runtime.manager import DependencyManager
from .runtime.scope import ScopeHandle

if TYPE_CHECKING:
    from .contracts import DependencyProvider
    from .models import Namespace
    from .type_vars import T


@dataclass(slots=True)
class Container:
    """
    Runtime dependency injection container.

    Container provides dependency registration and resolution.

    Design goals:
        - low-overhead runtime resolution
        - async-safe dependency initialization
        - deterministic dependency lifecycle
        - runtime graph diagnostics

    Threading model:
        Container is NOT thread-safe.

        Container assumes ownership by a single scheduler
        (event loop, actor runtime or dispatcher).

        Concurrent access from multiple tasks within the same scheduler
        is supported.

        Concurrent dependency initialization of the same dependency
        is coordinated through Future memoization.

        Access from multiple threads is NOT supported.

    Recommended usage:
        Single runtime kernel:
            Runtime Kernel
                └── Container
            The kernel owns the container and all dependency
            resolution is performed through the kernel.

        Multithreaded runtime:
            Worker #1
                └── Container
            Worker #2
                └── Container
            Each worker owns its own container instance.

    Notes:
        Thread safety is intentionally delegated to the runtime architecture.

        Container avoids internal locking by design.

        Introducing a global lock would reduce concurrency
        and potentially create a runtime bottleneck under load.

        If a single container must be shared between multiple execution
        contexts, access should therefore be serialized externally by
        a runtime dispatcher, actor mailbox, scheduler or message bus.

    """

    _manager: DependencyManager = field(default_factory=DependencyManager)
    _diagnostics: ContainerDiagnostics = field(init=False)

    def __post_init__(self) -> None:
        """
        Initialize runtime diagnostics facade.

        Diagnostics depend on the already constructed
        DependencyManager instance.
        """
        self._diagnostics = ContainerDiagnostics(self._manager)

    def register(
        self,
        *,
        contract: type[T],
        provider: DependencyProvider[T],
        namespace: str | Namespace,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        scope: DependencyScope = DependencyScope.TRANSIENT,
        overwrite: bool = False,
    ) -> None:
        """Register dependency in container."""
        self._manager.register(
            contract=contract,
            provider=provider,
            namespace=Namespace.parse(namespace),
            visibility=visibility,
            scope=scope,
            overwrite=overwrite,
        )

    async def resolve(
        self,
        contract: type[T],
        *,
        namespace: str | Namespace,  # owner
        requester: str | Namespace,  # caller
    ) -> T:
        """
        Resolve registered dependency instance.

        Args:
            contract:
                Dependency contract type.
            namespace:
                Dependency owner namespace.
            requester:
                Dependency requester namespace.

        Returns:
            resolved dependency instance

        """
        return await self._manager.resolve(
            contract=contract,
            namespace=Namespace.parse(namespace),
            requester=Namespace.parse(requester),
        )

    def scope(self) -> ScopeHandle:
        """
        Create async scope context manager.

        Examples:
            async with container.scope():
                ...

        Returns:
            async scope context manager

        """
        return ScopeHandle(
            scopes=self._manager.scopes,
            context=self._manager.context,
        )

    @property
    def diagnostics(self) -> ContainerDiagnostics:
        """Diagnostics API."""
        return self._diagnostics
