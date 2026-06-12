"""Runtime dependency manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar

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
    ScopeID,
)
from template_app.runtime.container.providers import FactoryProvider
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope_manager import ScopeManager
from template_app.runtime.container.visibility import enforce_visibility

if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.visibility import (
        DependencyVisibility,
    )


class ScopeHandle:
    def __init__(self, manager: ScopeManager) -> None:
        self._manager = manager
        self._scope_id: ScopeID | None = None

    def __aenter__(self) -> ScopeID:
        self._scope_id = self._manager.create_scope()
        return self._scope_id

    def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._scope_id is not None

        self._manager.close_scope(self._scope_id)


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
        *,
        contract: type[T],
        provider: FactoryProvider,
        namespace: Namespace,
        visibility: DependencyVisibility,
        scope: DependencyScope,
        overwrite: bool,
    ) -> None:
        """Register dependency metadata."""
        # if not isinstance(contract, type):
        #     raise InvalidContractError(contract)
        #
        # if not isinstance(provider, DependencyProvider):
        #     raise InvalidProviderError(provider)

        dependency_id = DependencyID(
            namespace=namespace,
            contract=contract,
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
        """Create runtime scope."""
        return self._scopes.create_scope()

    def close_scope(self, scope_id: ScopeID) -> None:
        """Destroy runtime scope."""
        self._scopes.close_scope(scope_id)

    def scopes(self) -> ScopeHandle:
        return ScopeHandle(self._scopes)

    ############
    # Resolution
    ############
    async def resolve(
        self,
        dependency_id: DependencyID,
        *,
        requester_ns: Namespace | None = None,
        scope_id: ScopeID | None = None,
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

        self._register_graph_edge(dependency_id)

        try:
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

        finally:
            self._resolution_stack.pop()  # TODO: check

    ####################
    # Internal lifecycle
    ####################

    async def _resolve_singleton(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor,
    ):

        if dependency_id not in self._singletons:
            instance = await descriptor.provider.provide(self)

            self._singletons[dependency_id] = instance

        return self._singletons[dependency_id]

    async def _resolve_scoped(
        self,
        dependency_id: DependencyID,
        descriptor: DependencyDescriptor,
        scope_id: ScopeID | None,
    ):

        if scope_id is None:
            msg = f"{dependency_id.contract.__name__} requires scope"
            raise ScopeRequiredError(msg)

        if not self._scopes.exists(scope_id):
            msg = "Scope is closed"
            raise ScopeRequiredError(msg)

        scope = self._scopes.get_scope(scope_id)

        if scope.contains(dependency_id):
            return scope.get(dependency_id)

        instance = await descriptor.provider.provide(self)

        scope.set(dependency_id, instance)

        return instance

    async def _resolve_transient(self, descriptor: DependencyDescriptor):
        return await descriptor.provider.provide(self)

    # async def _create_instance(
    #     self,
    #     descriptor: DependencyDescriptor,
    #     scope_id: ScopeID | None,
    # ):
    #     return await descriptor.provider.provide(self)

    def _register_graph_edge(self, dependency_id: DependencyID) -> None:
        """Build runtime dependency graph."""
        contract = dependency_id.contract

        if contract in self._resolution_stack:
            msg = " -> ".join(
                item.__name__ for item in (*self._resolution_stack, contract)
            )
            raise DependencyCycleError(msg)

        if self._resolution_stack:
            parent = self._resolution_stack[-1]
            self._graph.add_edge(parent.__name__, dependency_id)

        else:
            self._graph.add_node(dependency_id)

        self._resolution_stack.append(dependency_id)

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
