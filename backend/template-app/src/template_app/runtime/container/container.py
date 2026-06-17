"""Runtime dependency injection container."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.diagnostics.diagnostics import (
    ContainerDiagnostics,
)
from template_app.runtime.container.models.scope import DependencyScope
from template_app.runtime.container.models.visibility import (
    DependencyVisibility,
)
from template_app.runtime.container.runtime.helpers.scope import (
    ScopeHandle,
)
from template_app.runtime.container.runtime.manager import DependencyManager

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.type_vars import T


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

        Container assumes ownership by a single runtime scheduler
        and execution context.

        Concurrent dependency initialization is coordinated through
        Future memoization and delegated to the owning runtime architecture.

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
        self._diagnostics = ContainerDiagnostics(self._manager)

    def register(
        self,
        *,
        contract: type[T],
        provider: DependencyProvider[T],
        namespace: Namespace,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        scope: DependencyScope = DependencyScope.TRANSIENT,
        overwrite: bool = False,
    ) -> None:
        """Register dependency in container."""
        self._manager.register(
            contract=contract,
            provider=provider,
            namespace=namespace,
            visibility=visibility,
            scope=scope,
            overwrite=overwrite,
        )

    async def resolve(
        self,
        contract: type[T],
        *,
        namespace: Namespace,
    ) -> T:
        """
        Resolve registered dependency.

        Returns:
            resolved dependency

        """
        return await self._manager.resolve(
            contract=contract,
            namespace=namespace,
        )

    def scope(self) -> ScopeHandle:
        """
        Create async scope context manager.

        Examples:
            async with container.scope():
                logger = await container.resolve(Logger)

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
