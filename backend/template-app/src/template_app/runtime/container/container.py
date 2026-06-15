"""Public DI facade."""

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
from template_app.runtime.container.runtime.helpers.scope import ScopeHandle
from template_app.runtime.container.runtime.manager import DependencyManager

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.type_vars import T


@dataclass(slots=True)
class Container:
    """
    Public DI API.

    DependencyManager:
        responsible for DI system work, DI orchestrator
    ContainerDiagnostics:
        responsible for DI system inspecting.

    """

    _manager: DependencyManager = field(
        default_factory=DependencyManager,
    )
    _diagnostics: ContainerDiagnostics = field(init=False)

    def __post_init__(self) -> None:
        self._diagnostics = ContainerDiagnostics(self._manager)

    # delegate to Registry
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

    # delegate to manager
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

    # for ScopeManager existing separately
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

    # for diagnostics
    @property
    def diagnostics(self) -> ContainerDiagnostics:
        """Diagnostics API."""
        return self._diagnostics
