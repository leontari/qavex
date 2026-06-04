"""DI container."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar, cast

from .graph import DependencyNode
from .types import ContainerKey, DependencyContract, DependencyScope

if TYPE_CHECKING:
    from .contracts import DependencyProvider

T = TypeVar("T")

DEFAULT_NAMESPACE = "core"


@dataclass(slots=True)
class Container:
    """Runtime dependency container."""

    _providers: dict[ContainerKey, DependencyProvider] = field(
        default_factory=dict,
    )
    _singletons: dict[ContainerKey, object] = field(
        default_factory=dict,
    )

    def register(
        self,
        contract: DependencyContract,
        provider: DependencyProvider,
        namespace: str = DEFAULT_NAMESPACE,
    ) -> None:
        """Register dependency provider."""
        key = (namespace, contract)

        self._providers[key] = provider

    def resolve(
        self,
        contract: type[T],
        namespace: str = DEFAULT_NAMESPACE,
    ) -> T:
        """
        Resolve dependency.

        Returns:
            Dependency instance.

        """
        key = (namespace, contract)

        try:
            provider = self._providers[key]

        except KeyError as error:
            msg = f"Dependency not registered: {namespace}:{contract.__name__}"
            raise LookupError(msg) from error

        if provider.scope == DependencyScope.SINGLETON:
            if key not in self._singletons:
                self._singletons[key] = provider.provide(self)

            return cast("T", self._singletons[key])

        return cast("T", provider.provide(self))

    def try_resolve(
        self,
        contract: type[T],
        namespace: str = DEFAULT_NAMESPACE,
    ) -> T | None:
        """
        Resolve dependency safely.

        Returns:
            Dependency instance or None.

        """
        try:
            return self.resolve(contract, namespace)
        except LookupError:
            return None

    def contains(
        self,
        contract: DependencyContract,
        namespace: str = DEFAULT_NAMESPACE,
    ) -> bool:
        """
        Check dependency existence.

        Returns:
            True if dependency exists.

        """
        return (namespace, contract) in self._providers

    def snapshot(self) -> tuple[DependencyNode, ...]:
        """
        Build dependency graph snapshot.

        Returns:
            Immutable dependency graph.

        """
        return tuple(
            DependencyNode(
                namespace=namespace,
                contract=contract,
                scope=provider.scope,
            )
            for (
                namespace,
                contract,
            ), provider in self._providers.items()
        )
