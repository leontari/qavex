"""Runtime dependency manager."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import (
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
from template_app.runtime.container.runtime.helpers.resolution import (
    ResolutionContextManager,
)
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope_manager import (
    ScopeManager,
)
from template_app.runtime.container.runtime.singleton_cache import (
    SingletonCache,
)
from template_app.runtime.container.type_vars import T
from template_app.runtime.container.visibility_enforcer import (
    enforce_visibility,
)

if TYPE_CHECKING:
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

    Orchestrator only

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

    Registry:
        Source of truth for metadata registration.
    ScopeManager:
        Source of truth for scoped instances.
    SingletonCache:
        Source of truth for singleton instances.
    ResolutionContextManager:
        Source of truth for runtime context.
    RuntimeGraph:
        Source of truth for observed dependency relations.
    DependencyManager:
        Orchestrator only.

    """

    _registry: DependencyRegistry = field(
        default_factory=DependencyRegistry,
    )

    _graph: DependencyGraph = field(
        default_factory=DependencyGraph,
    )

    _context: ResolutionContextManager = field(
        default_factory=ResolutionContextManager,
    )

    _scopes: ScopeManager = field(
        default_factory=ScopeManager,
    )

    _singletons: SingletonCache = field(default_factory=SingletonCache)

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

    ############
    # Resolution
    ############
    async def resolve(
        self,
        *,
        contract: type[T],
        namespace: Namespace,
        scope_id: ScopeID,
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
        dependency_id = DependencyID(contract=contract, namespace=namespace)
        scope_id = scope_id or self._context.current.scope_id

        return await self._resolve_dependency(
            dependency_id=dependency_id,
            requester_ns=namespace,
            scope_id=scope_id,
        )

    async def _resolve_dependency(
        self,
        *,
        dependency_id: DependencyID,
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

        token = self._context.enter_resolution(dependency_id)

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
            self._context.leave_resolution(token)

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
        if self._singletons.contains(dependency_id):
            return self._singletons.get(dependency_id)

        # 2. check if initialization already in progress
        future = self._singletons.get_future(dependency_id)

        if future is not None:
            return await future

        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._singletons.set_future(dependency_id, future)

        # we are the "initializer"
        try:
            instance = await descriptor.provider.provide(self)

            self._singletons.set(dependency_id, instance)

            future.set_result(instance)
            return instance

        except Exception as error:
            future.set_exception(error)
            raise

        finally:
            # cleanup in-flight marker
            self._singletons.remove_future(dependency_id)

    async def _resolve_scoped(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor,
        scope_id: ScopeID,
    ):
        """Per-scope future memoization."""
        if scope_id is None:
            msg = f"{dependency_id.contract.__name__} requires scope"
            raise ScopeRequiredError(msg)

        # TODO: check logic
        if not self._scopes.exists(scope_id):
            msg = f"Scope {scope_id} not found for {dependency_id}."
            raise ScopeNotFoundError(msg)

        if self._scopes.contains(scope_id, dependency_id):
            return self._scopes.get(scope_id, dependency_id)

        future = self._scopes.get_future(scope_id, dependency_id)

        if future is not None:
            return await future

        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._scopes.set_future(scope_id, dependency_id, future)

        try:
            instance = await descriptor.provider.provide(self)

            self._scopes.set(scope_id, dependency_id, instance)
            future.set_result(instance)

            return instance

        except Exception as error:
            future.set_exception(error)
            raise

        finally:
            self._scopes.remove_future(scope_id, dependency_id)

    async def _resolve_transient(self, descriptor: DependencyDescriptor):
        """Call dependency provider directly."""
        return await descriptor.provider.provide(self)

    ################
    # Graph tracking
    ################

    def _register_graph_edge(self, dependency_id: DependencyID) -> None:
        """Build runtime dependency graph."""
        stack = self._context.current.stack

        if len(stack) >= 2:
            parent = stack[-1]
            self._graph.add_edge(parent, dependency_id)
        else:
            self._graph.add_node(dependency_id)

    ############
    # Validation
    ############

    # TODO: check whether it's necessary
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
        """Dependency metadata storage."""
        return self._registry

    @property
    def graph(self) -> DependencyGraph:
        """Dependency resolution history."""
        return self._graph

    @property
    def scopes(self) -> ScopeManager:
        """Scopes lifecycle service."""
        return self._scopes

    @property
    def singletons(self) -> SingletonCache:
        """Singleton cache runtime service."""
        return self._singletons

    @property
    def context(self) -> ResolutionContextManager:
        """Runtime resolution context manager."""
        return self._context

    #########
    # Testing
    #########
    def clear_singletons(self) -> None:
        self._singletons.clear()
