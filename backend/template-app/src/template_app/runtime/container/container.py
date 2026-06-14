"""Public DI facade."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.diagnostics.diagnostics import (
    ContainerDiagnostics,
)
from template_app.runtime.container.models.scope import (
    DependencyScope,
)
from template_app.runtime.container.models.visibility import (
    DependencyVisibility,
)
from template_app.runtime.container.runtime.manager import (
    DependencyManager,
    ScopeHandle,
)

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import (
        ScopeID,
    )
    from template_app.runtime.container.type_vars import T


@dataclass(slots=True)
class Container:
    """Public DI API."""

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
        scope_id: ScopeID | None = None,
    ) -> T:
        """
        Resolve registered dependency.

        Returns:
            resolved dependency

        """
        return await self._manager.resolve(
            contract=contract,
            namespace=namespace,
            scope_id=scope_id,
        )

    # for ScopeManager existing separately
    def create_scope(self) -> ScopeID:
        return self._manager.create_scope()

    # for ScopeManager existing separately
    def close_scope(self, scope: ScopeID) -> None:
        self._manager.close_scope(scope)

    def scope(self) -> ScopeHandle:
        return self._manager.scope()

    # for diagnostics
    @property
    def diagnostics(self) -> ContainerDiagnostics:
        """Diagnostics API."""
        return self._diagnostics
