"""Runtime dependency manager."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

from template_app.runtime.container.exceptions import (
    InvalidContractError,
    InvalidProviderError,
    ScopeClosedError,
    ScopeRequiredError,
    UnsupportedScopeError,
)
from template_app.runtime.container.models.dependency import (
    DependencyDescriptor,
    DependencyID,
)
from template_app.runtime.container.models.scope import (
    DependencyScope,
    ScopeState,
)
from template_app.runtime.container.runtime.graph import DependencyGraph
from template_app.runtime.container.runtime.helpers.context_manager import (
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
    DI orchestrator.

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
    ) -> T:
        """
        Resolve dependency instance.

        Implements DependencyResolver.

        Args:
            contract:
            namespace:

        Returns:
            Resolved dependency instance.

        """
        dependency_id = DependencyID(contract=contract, namespace=namespace)

        return cast(
            "T",
            await self._resolve_dependency(
                dependency_id=dependency_id,
                requester_ns=namespace,
            ),
        )

    async def _resolve_dependency(
        self,
        *,
        dependency_id: DependencyID,
        requester_ns: Namespace,
    ) -> T:
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
                    )
                case DependencyScope.TRANSIENT:
                    return await self._resolve_transient(
                        descriptor,
                    )

            raise UnsupportedScopeError(descriptor.scope)

        finally:
            self._context.leave_resolution(token)

    ####################
    # Internal lifecycle
    ####################

    async def _resolve_singleton(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor[T],
    ) -> T:
        """
        Resolve singleton dependency.

        Uses future memoization to prevent
        concurrent duplicate initialization.

        The first resolver initializes the dependency.
        Concurrent resolvers await the same initialization
        future and receive the same instance.

        Args:
            dependency_id:
                Dependency identifier.

            descriptor:
                Registered dependency descriptor.

        Returns:
            Singleton dependency instance.

        Raises:
            Any exception raised by provider.provide()

        """
        # 1. fast path (already initialized)
        if self._singletons.contains(dependency_id):
            return self._singletons.get(dependency_id)

        # 2. check if initialization already in progress
        loop = asyncio.get_running_loop()

        future, created = self._singletons.get_or_create_future(
            dependency_id,
            loop=loop,
        )
        if not created:
            return await future

        # 3. we are the "initializer"
        try:
            instance = await descriptor.provider.provide(self)
            self._singletons.set(dependency_id, instance)

            if not future.done():
                future.set_result(instance)

            return instance

        except BaseException as error:
            if not future.done():
                future.set_exception(error)
            raise

        finally:
            # cleanup in-flight marker
            self._singletons.remove_future(dependency_id)

    async def _resolve_scoped(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor[T],
    ) -> T:
        """
        Resolve scoped dependency.

        Uses per-scop future memoization to prevent
        concurrent duplicate initialization.

        Scoped instances are reused only within the currently active scope.

        Args:
            dependency_id:
                Dependency identifier.
            descriptor:
                Registered dependency descriptor.

        Returns:
            Scoped dependency instance.

        Raises:
            ScopeRequiredError:
                If no active scope exists.
            ScopeClosedError:
                If scope is not active.
            Any exception raised by provider.provide().

        """
        scope_id = self._context.current.scope_id

        if scope_id is None:
            raise ScopeRequiredError(dependency_id)

        scope = self._scopes.get_scope(scope_id)

        if scope.state is not ScopeState.ACTIVE:
            raise ScopeClosedError(scope_id)

        if scope.contains(dependency_id):
            return scope.get(dependency_id)

        loop = asyncio.get_running_loop()

        future, created = scope.get_or_create_future(dependency_id, loop=loop)

        if not created:
            return await future

        try:
            instance = await descriptor.provider.provide(self)
            scope.set(dependency_id, instance)

            if not future.done():
                future.set_result(instance)

            return instance

        except BaseException as error:
            if not future.done():
                future.set_exception(error)
            raise

        finally:
            scope.remove_future(dependency_id)

    async def _resolve_transient(
        self,
        descriptor: DependencyDescriptor[T],
    ) -> T:
        """
        Resolve transient dependency.

        Transient dependencies are never cached.
        Provider is executed on every resolution.

        Args:
            descriptor:
                Registered dependency descriptor.

        Returns:
            Newly created dependency instance.

        Raises:
            Any exception raised by provider.provide().

        """
        return await descriptor.provider.provide(self)

    ################
    # Graph tracking
    ################

    def _register_graph_edge(self, dependency_id: DependencyID) -> None:
        """Register runtime dependency relation."""
        stack = self._context.current.stack

        if len(stack) >= 2:
            parent = stack[-2]
            self._graph.add_edge(parent, dependency_id)
        else:
            self._graph.add_node(dependency_id)

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
