"""Runtime dependency manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar, cast

from .contracts import DependencyProvider
from .exceptions import (
    AsyncDependencyError,
    DependencyCycleError,
    InvalidProviderError,
    ScopeRequiredError,
    DependencyVisibilityError,
)
from .namespace import Namespace
from .registry import DependencyRegistry
from .scope import ScopeContext
from .types import (
    DependencyScope,
    DependencyVisibility,
)
from .visibility import enforce_visibility

if TYPE_CHECKING:
    from .graph import DependencyGraph

T = TypeVar("T")


@dataclass(slots=True)
class DependencyManager:
    """
    Runtime dependency manager.

    Responsibilities:
        - dependency registration
        - singleton lifecycle
        - scoped lifecycle
        - dependency resolution
        - async dependency resolution
        - visibility enforcement
        - namespace enforcement
        - diagnostics

    Does not store dependencies directly.
    Registry owns metadata.
    Manager owns runtime lifecycle.
    """

    _registry: DependencyRegistry = field(
        default_factory=DependencyRegistry,
    )

    _singletons: dict[tuple[str, type[Any]], object] = field(
        default_factory=dict,
    )
    _resolution_stack: list[type[Any]] = field(
        default_factory=list,
    )

    def register(
        self,
        contract: type[Any],
        provider: DependencyProvider,
        *,
        namespace: Namespace,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency.

        Args:
            contract:
                Dependency contract.

            provider:
                Dependency provider.

            namespace:
                Dependency namespace.

            visibility:
                Dependency visibility.

            overwrite:
                Allow to overwrite.

        """
        if not isinstance(provider, DependencyProvider):
            msg = f"{type(provider).__name__} is not a DependencyProvider"
            raise InvalidProviderError(msg)

        self._registry.register(
            namespace=namespace,
            contract=contract,
            provider=provider,
            visibility=visibility,
            overwrite=overwrite,
        )

    def resolve(
        self,
        contract: type[T],
        *,
        requester: Namespace | None = None,
        scope: ScopeContext | None = None,
    ) -> T:
        """
        Resolve dependency.

        Args:
            contract:
                Dependency contract.

            requester:
                Namespace requesting dependency.

            scope:
                Optional scope context.

        Returns:
            Resolved dependency.

        """
        descriptor = self._registry.find(contract)
        requester_ns = requester or Namespace("kernel")

        enforce_visibility(
            owner=descriptor.namespace,
            requester=requester_ns,
            visibility=descriptor.visibility,
        )

        provider = descriptor.provider

        if provider.scope is DependencyScope.ASYNC:
            msg = f"{contract.__name__} must be resolved via resolve_async()"
            raise AsyncDependencyError(msg)

        if contract in self._resolution_stack:
            chain = " -> ".join(
                item.__name__ for item in (*self._resolution_stack, contract)
            )
            raise DependencyCycleError(chain)

        self._resolution_stack.append(contract)

        # if descriptor.visibility is DependencyVisibility.PRIVATE:
        #     msg = f"{contract.__name__} is private"
        #     raise DependencyVisibilityError(msg)

        try:
            if provider.scope is DependencyScope.SCOPED:
                if scope is None:
                    msg = f"{contract.__name__} requires ScopeContext"
                    raise ScopeRequiredError(msg)

                if scope.contains(contract):
                    return cast("T", scope.get(contract))

                instance = provider.provide(self)
                scope.set(contract, instance)

                return cast("T", instance)

            key = (descriptor.namespace.name, contract)

            if provider.scope is DependencyScope.SINGLETON:
                if key not in self._singletons:
                    self._singletons[key] = provider.provide(self)

                return cast("T", self._singletons[key])

            return cast("T", provider.provide(self))

        finally:
            self._resolution_stack.pop()

    async def resolve_async(
        self,
        contract: type[T],
        *,
        requester: Namespace | None = None,
        scope: ScopeContext | None = None,
    ) -> T:
        """
        Resolve async dependency.

        Args:
            contract:
                Dependency contract.

            requester:
                Namespace requesting dependency.

            scope:
                Optional scope context.

        Returns:
            Resolved dependency.

        """
        descriptor = self._registry.find(contract)
        requester_ns = requester or Namespace("kernel")

        enforce_visibility(
            owner=descriptor.namespace,
            requester=requester_ns,
            visibility=descriptor.visibility,
        )

        provider = descriptor.provider

        if provider.scope is DependencyScope.SCOPED:
            if scope is None:
                msg = f"{contract.__name__} requires ScopeContext."
                raise ScopeRequiredError(msg)

            if scope.contains(contract):
                return cast("T", scope.get(contract))

            instance = provider.provide(self)
            scope.set(contract, instance)

            return cast("T", instance)

        if provider.scope is not DependencyScope.ASYNC:
            return cast("T", await provider.provide(self))

        return self.resolve(contract, requester=requester, scope=scope)

    def contains(self, contract: type[Any], *, namespace: str) -> bool:
        """
        Check dependency existence.

        Returns:
            bool

        """
        return self._registry.contains(namespace, contract)

    def snapshot(self) -> DependencyGraph:
        """
        Create diagnostics snapshot.

        Returns:
            DependencyGraph

        """
        return self._registry.snapshot()

    def dump(self) -> str:
        """
        Return Human readable graph.

        Returns:
            str

        """
        graph = self.snapshot()

        lines: list[str] = []

        current_namespace = ""

        for node in sorted(
            graph.nodes,
            key=lambda x: (x.namespace, x.contract),
        ):
            if node.namespace != current_namespace:
                current_namespace = node.namespace
                lines.append(current_namespace)

            lines.append(f"  └── {node.contract} [{node.scope}]")

        return "\n".join(lines)

    def clear_singletons(self) -> None:
        """
        Clear singleton cache.

        Useful in tests.
        """
        self._singletons.clear()
