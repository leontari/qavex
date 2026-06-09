"""Public DI facade."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar, cast

from template_app.runtime.container.models.dependency import DependencyID
from template_app.runtime.container.runtime.manager import (
    DependencyManager,
    ScopeHandle,
)

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import ScopeID
    from template_app.runtime.container.models.visibility import (
        DependencyVisibility,
    )
    from template_app.runtime.container.runtime.scope_manager import (
        ScopeManager,
    )

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class Container:
    """Public DI API."""

    manager: DependencyManager = field(default_factory=DependencyManager)

    # delegate to Registry
    def register(
        self,
        *,
        contract: type[Any],
        provider: DependencyProvider[Any],
        namespace: Namespace,
        visibility: DependencyVisibility,
    ) -> None:
        """Register dependency in container."""
        self.manager.register(
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
    async def close_scope(
        self,
        scope: ScopeID,
    ) -> None:
        await self.manager.close_scope(scope)

    def scopes(self) -> ScopeHandle:
        return self.manager.scopes()


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
