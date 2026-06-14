"""Runtime dependency manager."""

from __future__ import annotations

import asyncio
from asyncio import Future, get_running_loop
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import (
    DependencyCycleError,
    InvalidContractError,
    InvalidProviderError,
    ScopeNotFoundError,
    ScopeRequiredError,
)
from template_app.runtime.container.models.dependency import (
    DependencyDescriptor,
    DependencyID,
)
from template_app.runtime.container.models.scope import (
    DependencyScope,
    ScopeID,
)
from template_app.runtime.container.runtime.graph import DependencyGraph
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope_manager import (
    ScopeHandle,
    ScopeManager,
)
from template_app.runtime.container.type_vars import T
from template_app.runtime.container.visibility_enforcer import (
    enforce_visibility,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from template_app.runtime.container.contracts import (
        DependencyProvider,
    )
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.visibility import (
        DependencyVisibility,
    )


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

    DependencyManager: responsible for DI system work
    ContainerDiagnostics: responsible for DI system inspecting

    Registry: Source of truth for registration.
    ScopeManager: Source of truth for scoped instances.
    SingletonCache: Source of truth for singleton instances.
    RuntimeGraph: Source of truth for observed dependency relations.

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

    _scopes_futures: dict[tuple[ScopeID, DependencyID], Future] = field(
        default_factory=dict,
    )

    _singletons: dict[DependencyID, object] = field(
        default_factory=dict,
    )
    # in-flight initialization tracker
    _singleton_futures: dict[DependencyID, Future] = field(
        default_factory=dict,
    )

    _resolution_stack: ContextVar[tuple[DependencyID, ...]] = ContextVar(
        "dependency_resolution_stack",
        default=(),
    )

    ##############
    # Registration
    ##############

    def register(
        self,
        *,
        contract: type[T],
        provider: DependencyProvider[T],
        namespace: Namespace,
        visibility: DependencyVisibility,
        scope: DependencyScope,
        overwrite: bool,
    ) -> None:
        """Register dependency metadata."""
        if not isinstance(contract, type):  # TODO: check
            raise InvalidContractError(contract)

        provide = getattr(provider, "provide", None)
        if not callable(provide):
            raise InvalidProviderError(provider)

        dependency_id = DependencyID(
            contract=contract,
            namespace=namespace,
        )

        descriptor = DependencyDescriptor(
            ident=dependency_id,
            provider=provider,
            visibility=visibility,
            scope=scope,
        )

        if overwrite:
            self._registry.replace(descriptor=descriptor)
        else:
            self._registry.add(descriptor=descriptor)

    #################
    # Scope lifecycle
    #################

    def create_scope(self) -> ScopeID:
        """
        Create runtime scope.

        Low-level scpe API.

        Prefer using:
            async with container.scope()

        Returns:
            ScopeID

        """
        return self._scopes.create_scope()

    def close_scope(self, scope_id: ScopeID) -> None:
        """
        Destroy runtime scope.

        Low-level scpe API.

        Prefer using:
            async with container.scope()
        """
        self._scopes.close_scope(scope_id)

        # cleanup futures
        self._scopes_futures = {
            k: v for k, v in self._scopes_futures.items() if k[0] != scope_id
        }

    def scope(self) -> ScopeHandle:
        return ScopeHandle(self._scopes)

    ############
    # Resolution
    ############
    async def resolve(
        self,
        contract: type[T],
        *,
        namespace: Namespace,
        scope_id: ScopeID | None = None,
    ) -> T:
        """
        Resolve dependency instance.

        Implements DependencyResolver.

        Args:
            contract:
            namespace:
            scope_id:

        Returns:
            Resolved dependency instance.

        """
        dependency_id = DependencyID(
            contract=contract,
            namespace=namespace,
        )

        return await self._resolve_dependency(
            dependency_id=dependency_id,
            requester_ns=namespace,
            scope_id=scope_id,
        )

    async def _resolve_dependency(
        self,
        dependency_id: DependencyID,
        *,
        requester_ns: Namespace,
        scope_id: ScopeID,
    ) -> object:
        """
        Resolve dependency.

        Returns:
            Resolved dependency instance.

        """
        descriptor = self._registry.get(dependency_id)

        enforce_visibility(
            owner=descriptor.ident.namespace,
            requester=requester_ns or descriptor.ident.namespace,
            visibility=descriptor.visibility,
        )

        token = self._enter_resolution(dependency_id)

        try:
            self._register_graph_edge(dependency_id)

            match descriptor.scope:
                case DependencyScope.SINGLETON:
                    return await self._resolve_singleton(
                        dependency_id,
                        descriptor,
                    )
                case DependencyScope.SCOPED:
                    return await self._resolve_scoped(
                        dependency_id,
                        descriptor,
                        scope_id,
                    )
                case DependencyScope.TRANSIENT:
                    return await self._resolve_transient(
                        descriptor,
                    )

            msg = f"Unsupported dependency scope: {descriptor.scope}"
            raise RuntimeError(msg)

        finally:
            self._leave_resolution(token)

    ####################
    # Internal lifecycle
    ####################

    async def _resolve_singleton(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor,
    ):
        """Global future memoization."""
        # 1. fast path (already initialized)
        instance = self._singletons.get(dependency_id)
        if instance is not None:
            return instance

        # 2. check if initialization already in progress
        future = self._singleton_futures.get(dependency_id)
        if future is None:
            loop = get_running_loop()
            future = loop.create_future()
            self._singleton_futures[dependency_id] = future

            # we are the "initializer"
            try:
                instance = await descriptor.provider.provide(self)

                self._singletons[dependency_id] = instance

                future.set_result(instance)
                return instance

            except Exception as e:
                future.set_exception(e)
                raise

            finally:
                # cleanup in-flight marker
                await self._singleton_futures.pop(dependency_id, None)

        # 3. someone else is initializing -> wait for result
        return await future

    async def _resolve_scoped(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor,
        scope_id: ScopeID | None,
    ):
        """Per-scope future memoization."""
        if scope_id is None:
            msg = f"{dependency_id.contract.__name__} requires scope"
            raise ScopeRequiredError(msg)

        if not self._scopes.exists(scope_id):
            msg = f"Scope {scope_id} not found for {dependency_id}."
            raise ScopeNotFoundError(msg)

        scope = self._scopes.get_scope(scope_id)

        # fast path
        if scope.contains(dependency_id):
            return scope.get(dependency_id)

        key = (scope_id, dependency_id)

        future = self._scopes_futures.get(key)
        if future is None:
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            self._scopes_futures[key] = future

            try:
                instance = await descriptor.provider.provide(self)

                scope.set(dependency_id, instance)
                future.set_result(instance)
                return instance

            except Exception as e:
                future.set_exception(e)
                raise

            finally:
                await self._scopes_futures.pop(key, None)

        return await future

    async def _resolve_transient(self, descriptor: DependencyDescriptor):
        """Call dependency provider directly."""
        return await descriptor.provider.provide(self)

    ####################################
    # Resolution stack (cycle detection)
    ####################################

    def _enter_resolution(
        self,
        dependency_id: DependencyID,
    ) -> Token[tuple[DependencyID, ...]]:
        stack = self._resolution_stack.get()

        if dependency_id in stack:
            chain = " -> ".join(str(item) for item in (*stack, dependency_id))
            raise DependencyCycleError(chain)

        return self._resolution_stack.set(
            (*stack, dependency_id),
        )

    def _leave_resolution(
        self,
        token: Token[tuple[DependencyID, ...]],
    ) -> None:
        self._resolution_stack.reset(token)

    ################
    # Graph tracking
    ################

    def _register_graph_edge(self, dependency_id: DependencyID) -> None:
        """Build runtime dependency graph."""
        stack = self._resolution_stack.get()

        if stack:
            parent = stack[-1]
            self._graph.add_edge(parent, dependency_id)
        else:
            self._graph.add_node(dependency_id)

    ############
    # Validation
    ############

    def validate(self) -> None:
        """
        Validate currently observed runtime graph.

        Graph is built lazily during dependency resolution.

        Only dependencies that have been resolved at least once
        are present in the graph.
        """
        self._graph.validate()

    #############
    # Diagnostics
    #############

    @property
    def registry(self) -> DependencyRegistry:
        return self._registry

    @property
    def graph(self) -> DependencyGraph:
        return self._graph

    @property
    def scopes(self) -> ScopeManager:
        return self._scopes

    @property
    def singletons(self) -> Mapping[DependencyID, object]:
        return MappingProxyType(self._singletons)

    #########
    # Testing
    #########
    def clear_singletons(self) -> None:
        self._singletons.clear()
