"""Public DI facade."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import (
        ScopeID,
    )

T = TypeVar("T")


@dataclass(slots=True)
class Container:
    """Public DI API."""

    manager: DependencyManager = field(default_factory=DependencyManager)

    # delegate to Registry
    def register(
        self,
        contract: type[Any],
        provider: DependencyProvider[Any],
        *,
        namespace: Namespace | None = None,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        scope: DependencyScope = DependencyScope.TRANSIENT,
        overwrite: bool = False,
    ) -> None:
        """Register dependency in container."""
        self.manager.register(
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
            await self.manager.resolve(
                dependency_id=dependency_id,
                scope_id=scope,
            ),
        )

    # for ScopeManager existing separately
    def create_scope(self) -> ScopeID:
        return self.manager.create_scope()

    # for ScopeManager existing separately
    def close_scope(self, scope: ScopeID) -> None:
        self.manager.close_scope(scope)

    def scopes(self) -> ScopeHandle:
        return self.manager.scopes()
