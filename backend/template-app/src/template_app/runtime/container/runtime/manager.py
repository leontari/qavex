"""Runtime dependency manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

from template_app.runtime.container.contracts import DependencyProvider
from template_app.runtime.container.exceptions import (
    DependencyCycleError,
    InvalidProviderError,
    ScopeRequiredError,
)
from template_app.runtime.container.graph.diagnostics import ContainerSnapshot
from template_app.runtime.container.graph.graph import DependencyGraph
from template_app.runtime.container.models.dependency import (
    DependencyDescriptor,
    DependencyID,
)
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import (
    DependencyScope,
    ScopeContext,
    ScopeID,
)
from template_app.runtime.container.models.visibility import (
    DependencyVisibility,
)
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope_manager import ScopeManager
from template_app.runtime.container.visibility import enforce_visibility


class ScopeHandle:
    def __init__(self, manager: ScopeManager) -> None:
        self._manager = manager
        self._scope_id: ScopeID | None = None

    async def __aenter__(self) -> ScopeID:
        self._scope_id = self._manager.create_scope()
        return self._scope_id

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._scope_id is not None

        await self._manager.close_scope(self._scope_id)


T = TypeVar("T")


@dataclass(slots=True)
class DependencyManager:
    """
    Runtime orchestration layer.

    Owns:

        - registry
        - graph
        - scope lifecycle
        - singleton lifecycle

    Responsible for:

        - dependency resolution
        - visibility checks
        - graph construction
        - graph validation
    """

    _registry: DependencyRegistry = field(
        default_factory=DependencyRegistry,
    )

    _graph: DependencyGraph = field(
        default_factory=DependencyGraph,
    )

    _scopes: ScopeManager = field(
        default_factory=ScopeManager,
    )

    _singletons: dict[DependencyID:object] = field(
        default_factory=dict,
    )

    _resolution_stack: list[DependencyID] = field(
        default_factory=list,
    )

    ##############
    # Registration
    ##############

    def register(
        self,
        contract: type[Any],
        provider: DependencyProvider[Any],
        *,
        namespace: Namespace,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency.

        Public api.

        Delegates registration to registry.
        """
        if not isinstance(provider, DependencyProvider):
            msg = f"{type(provider).__name__} is not DependencyProvider"
            raise InvalidProviderError(msg)

        descriptor = DependencyDescriptor(
            contract=contract,
            provider=provider,
            namespace=namespace,
            visibility=visibility,
        )

        self._registry.register(
            descriptor=descriptor,
            overwrite=overwrite,
        )

    #################
    # Scope lifecycle
    #################

    def create_scope(self) -> ScopeContext:
        """Create runtime scope."""
        return self._scopes.create_scope()

    def close_scope(self, scope_id: ScopeID) -> None:
        """Destroy runtime scope."""
        self._scopes.close_scope(scope_id)

    def scopes(self):
        return ScopeHandle(self._scopes)

    ############
    # Resolution
    ############
    async def resolve(
        self,
        dependency_id: DependencyID,
        scope_id: ScopeID | None,
    ) -> T:

        scope = self._scopes.get_scope(scope_id)

        if scope.contains(dependency_id):
            return scope.get(dependency_id)

        instance = await self._create_instance(...)

        scope.set(dependency_id, instance)

        return instance

    async def resolve_(
        self,
        contract: type[T],
        *,
        requester: Namespace | None = None,
        scope_id: ScopeID | None = None,
    ) -> T:
        """Resolve dependency."""

        descriptor = self._registry.get(contract)

        owner_namespace = descriptor.namespace
        requester_namespace = requester or Namespace("kernel")  # TODO: check

        enforce_visibility(
            owner=owner_namespace,
            requester=requester_namespace,
            visibility=descriptor.visibility,
        )

        self._register_graph_edge(contract)

        try:
            provider = descriptor.provider

            if provider.scope is DependencyScope.SCOPED:
                return await self._resolve_scoped(descriptor, scope_id)

            if provider.scope is DependencyScope.SINGLETON:
                return await self._resolve_singleton(descriptor)

            if provider.scope is DependencyScope.TRANSIENT:
                return await provider.provide(self)

        finally:
            self._resolution_stack.pop()  # TODO: check

    ####################
    # Internal lifecycle
    ####################

    async def _resolve_singleton(self, descriptor: DependencyDescriptor):

        key = descriptor.namespace.name, descriptor.contract

        if key not in self._singletons:
            instance = await descriptor.provider.provide(self)

            self._singletons[key] = instance

        return self._singletons[key]

    async def _resolve_scoped(
        self,
        descriptor: DependencyDescriptor,
        scope_id: ScopeID | None,
    ):

        if scope_id is None:
            msg = f"{descriptor.contract.__name__} requires scope"
            raise ScopeRequiredError(msg)

        if not self._scopes.exists(scope_id):
            msg = "Scope is closed"
            raise ScopeRequiredError(msg)

        scope = self._scopes.get_scope(scope_id)

        key = descriptor.namespace.name, descriptor.contract

        if scope.contains(key):
            return scope.get(key)

        instance = await descriptor.provider.provide(self)

        scope.set(key, instance)

        return instance

    def _register_graph_edge(self, contract: type[Any]) -> None:
        """Build runtime dependency graph."""
        if contract in self._resolution_stack:
            msg = " -> ".join(
                item.__name__ for item in (*self._resolution_stack, contract)
            )
            raise DependencyCycleError(msg)

        if self._resolution_stack:
            parent = self._resolution_stack[-1]
            self._graph.add_edge(parent.__name__, contract.__name__)

        else:
            self._graph.add_node(contract.__name__)

        self._resolution_stack.append(contract)

    ############
    # Validation
    ############

    def validate(self) -> None:
        """Validate runtime graph."""
        self._graph.validate()

    #############
    # Diagnostics
    #############

    def snapshot(self):
        return ContainerSnapshot(graph=self._graph)

    def graph(self) -> DependencyGraph:
        return self._graph

    #########
    # Testing
    #########

    def clear_singletons(self) -> None:
        self._singletons.clear()


# @dataclass(slots=True)
# class DependencyManager:
#     """
#     Runtime dependency resolver.
#
#     Responsible for dependency construction,
#     lifecycle handling and dependency graph traversal.
#
#     Does not expose public container API.
#     """
#
#     registry: Registry
#     scopes: ScopeManager
#
#     # single main operation. That is all.
#     async def resolve(
#         self,
#         key: DependencyId,
#         scope: ScopeID | None = None,
#     ) -> object: ...
#         # get registration
#         descriptor = registry.get(key)
#
#         # verify lifetime
#         # SINGLETON
#         # SCOPED
#         # TRANSIENT
#
#         # search in cache
#         # Singleton:
#         singleton_cache.get(key)
#         # Scoped:
#         # scope.get(key)
#
#         # create instance
#         instance = await provider.create(...)
#
#         # save in cache
#         signleton_cache[key] = instance
#         # or
#         scope[key] = instance
#
#         # return result
#         return instance
#
#
#     ###############
#     # INNER METHODS
#     ###############
#         async def _resolve_singleton(self): ...
#         async def _resolve_scoped(self): ...
#         async def _resolve_transient(self): ...
#         async def _create_instance(self): ...
#
#     ######
#     # we have dependency graph, so manager should construct ResolutionContext
#     ######
#         # example:
# async def _create_instance(...):
#     ResolutionContext(stack=[])
#     # and then watches for cycles like
#     UserService -> UserRepository -> Database
#
#
# #########################
# # what should not be here
# #########################
# # registration like
# manager.register(...) -> it is Registry responsibility
#
# # scope management like
# manager.create_scope()
# manager.close_scope() -> it is ScopeManager responsibility
#
# # graph export like
# manager.export_mermaid() -> it is Graph responsibility
#
# # diagnostics like
# manager.snapshot() -> it is Diagnostics responsibility
