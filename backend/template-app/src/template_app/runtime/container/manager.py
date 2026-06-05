"""Runtime dependency manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar, cast

from .exceptions import DependencyVisibilityError
from .registry import DependencyRegistry
from .types import DependencyScope, DependencyVisibility

if TYPE_CHECKING:
    from .graph import DependencyGraph

T = TypeVar("T")


@dataclass(slots=True)
class DependencyManager:
    """
    Runtime dependency manager.

    Responsibilities:
        - registration
        - singleton lifecycle
        - dependency resolution
        - diagnostics

    Does not store dependencies directly.
    """

    registry: DependencyRegistry = field(
        default_factory=DependencyRegistry,
    )

    _singletons: dict[tuple[str, type[Any]], object] = field(
        default_factory=dict,
    )

    def register(
        self,
        contract: type[Any],
        provider: Any,
        *,
        namespace: str,
        visibility: DependencyVisibility = DependencyVisibility.PUBLIC,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency.

        Args:
            contract:
                Dependency contract.

            provider:
                Provider.

            namespace:
                Namespace.

            visibility:
                Visibility.

            overwrite:
                Allow to overwrite.

        """
        self.registry.register(
            namespace=namespace,
            contract=contract,
            provider=provider,
            visibility=visibility,
            overwrite=overwrite,
        )

    # def resolve(
    #     self,
    #     contract: type[T],
    #     *,
    #     namespace: str
    # ) -> T:
    def resolve(
        self,
        contract: type[T],
        *,
        owner: Namespace,
        requester: Namespace,
        scope: ScopeContext | None = None,
    ) -> T:
        """
        Resolve dependency.

        Args:
            contract:
                Dependency contract.

            namespace:
                Namespace.

        Returns:
            T

        """
        descriptor = self.registry.get(namespace, contract)

        if descriptor.visibility is DependencyVisibility.PRIVATE:
            msg = f"{contract.__name__} is private"
            raise DependencyVisibilityError(msg)

        provider = descriptor.provider

        key = (namespace, contract)

        if provider.scope is DependencyScope.SINGLETON:
            if key not in self._singletons:
                self._singletons[key] = provider.provide(self)

            return cast("T", self._singletons[key])

        return cast("T", provider.provide(self))

    async def resolve_async(
        self,
        contract: type[T],
        *,
        namespace: Namespace | None = None,
        scope: ScopeContext | None = None,
    ) -> T:
        """
        Resolve async dependency.

        Returns:
            T

        """
        descriptor = self.registry.get(namespace, contract)

        provider = descriptor.provider

        if provider.scope is not DependencyScope.ASYNC:
            return self.resolve(contract, namespace=namespace)

        result = await provider.provide(self)

        return cast("T", result)

    def contains(self, contract: type[Any], *, namespace: str) -> bool:
        """
        Check dependency existence.

        Returns:
            bool

        """
        return self.registry.contains(namespace, contract)

    def snapshot(self) -> DependencyGraph:
        """
        Dependency graph snapshot.

        Returns:
            DependencyGraph

        """
        return self.registry.snapshot()

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
