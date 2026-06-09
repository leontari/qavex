from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar, cast

from template_app.runtime.container.models.dependency import DependencyID

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import ScopeID
    from template_app.runtime.container.models.visibility import (
        DependencyVisibility,
    )
    from template_app.runtime.container.runtime.manager import (
        DependencyManager,
    )
    from template_app.runtime.container.runtime.registry import (
        DependencyRegistry,
    )
    from template_app.runtime.container.runtime.scope_manager import (
        ScopeManager,
    )

T = TypeVar("T")


@dataclass(slots=True)
class Container:
    """
    Public DI facade.

    Coordinates registry,
    dependency resolution and scopes.
    """

    registry: DependencyRegistry
    manager: DependencyManager
    scopes: ScopeManager

    # delegate to Registry
    def register(
        self,
        *,
        contract: type[Any],
        provider: DependencyProvider[Any],
        namespace: Namespace,
        visibility: DependencyVisibility,
    ) -> None:
        self.registry.register(
            contract=contract,
            provider=provider,
            namespace=namespace,
            visibility=visibility,
        )

    # delegate to manager
    async def resolve(
        self,
        contract: type[T],
        *,
        namespace: Namespace,
        scope: ScopeID | None = None,
    ) -> T:
        key = DependencyID(
            namespace=namespace,
            contract=contract,
        )
        return cast(
            "T",
            await self.manager.resolve(
                key=key,
                scope=scope,
            ),
        )

    # for ScopeManager existing separately
    def create_scope(self) -> ScopeID:
        return self.scopes.create_scope()

    # for ScopeManager existing separately
    async def close_scope(
        self,
        scope: ScopeID,
    ) -> None:
        await self.scopes.close_scope(scope)


# # Very useful to make
# # async with container.scope() as scope:
# #     service = await container.resolve(
# #         UserService,
# #         scope=scope,
# #     )
# # and then
# # class Container:
# #     def scope(self) -> ScopeHandle:
# #         return ScopeHandle(self.scopes)
#
#
# container = Container()
# # do not mix diagnostics with main API
# # it's better
# container.diagnostics.snapshot()
# or
# container.graph.export_mermaid()
# #
#
# #############
# # basic usage
# #############
# container.register(...)
#
# scope = container.create_scope()
#
# service = await container.resolve(
#     UserService,
#     scope=scope,
# )
#
#
# ############
# # target API
# ############
# container = Container()
#
# container.register(...)
#
# async with container.scope() as scope:
#     service = await container.resolve(
#         UserService,
#         scope=scope,
#     )
#
# # This should be considered as implementation and should not be touched directly
# #
# # Registry
# # DependencyManager
# # ScopeManager
# # DependencyGraph
