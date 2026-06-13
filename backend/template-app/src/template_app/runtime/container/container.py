"""Public DI facade."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

from template_app.runtime.container.diagnostics.diagnostics import (
    ContainerDiagnostics,
)
from template_app.runtime.container.models.dependency import (
    DependencyID,
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
    from template_app.runtime.container.diagnostics.snapshot import (
        ContainerSnapshot,
    )
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import (
        ScopeID,
    )
    from template_app.runtime.container.types import T


@dataclass(slots=True)
class Container:
    """Public DI API."""

    _manager: DependencyManager = field(
        default_factory=DependencyManager,
    )
    _diagnostics: ContainerDiagnostics = field(
        default_factory=ContainerDiagnostics,
    )

    # delegate to Registry
    def register(
        self,
        contract: type[T],
        provider: DependencyProvider[T],
        *,
        namespace: Namespace | None = None,
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
        namespace: Namespace,  # TODO: requester namespace
        scope: ScopeID | None = None,
    ) -> T:
        """
        Resolve registered dependency.

        Returns:
            resolved dependency

        """
        dependency_id = DependencyID(
            namespace=namespace,
            contract=contract,
        )

        return cast(
            "T",
            await self._manager.resolve(
                dependency_id=dependency_id,
                scope_id=scope,
            ),
        )

    # for ScopeManager existing separately
    def create_scope(self) -> ScopeID:
        return self._manager.create_scope()

    # for ScopeManager existing separately
    def close_scope(self, scope: ScopeID) -> None:
        self._manager.close_scope(scope)

    def scopes(self) -> ScopeHandle:
        return self._manager.scope()

    # for diagnostics
    @property
    def diagnostics(self) -> ContainerSnapshot:
        """Read-only diagnostics API."""
        return self._diagnostics.snapshot
