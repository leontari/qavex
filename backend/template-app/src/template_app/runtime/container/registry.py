from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)
from .graph import DependencyGraph, DependencyNode
from .namespace import Namespace

if TYPE_CHECKING:
    from .contracts import DependencyProvider
    from .types import DependencyVisibility


@dataclass(slots=True, frozen=True)
class DependencyDescriptor:
    """Registered dependency descriptor."""

    contract: type[Any]
    provider: DependencyProvider
    namespace: Namespace
    visibility: DependencyVisibility


@dataclass(slots=True)
class DependencyRegistry:
    """
    Dependency storage.

    Responsibilities:
        - dependency ownership
        - namespace isolation
        - dependency metadata storage

    No resolve logic is allowed here.
    """

    _namespaces: dict[str, dict[type[Any], DependencyDescriptor]] = field(
        default_factory=dict,
    )

    def register(
        self,
        namespace: str,
        contract: type[Any],
        provider: DependencyProvider,
        visibility: DependencyVisibility,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency.

        Args:
            namespace:
                Namespace name.

            contract:
                Dependency contract.

            provider:
                Provider implementation.

            visibility:
                Dependency visibility.

            overwrite:
                Allow to overwrite.

        Raises:
            DependencyAlreadyRegisteredError

        """
        bucket = self._namespaces.setdefault(namespace, {})

        if contract in bucket and not overwrite:
            msg = f"{contract.__name__} already registered in '{namespace}'"
            raise DependencyAlreadyRegisteredError(msg)

        bucket[contract] = DependencyDescriptor(
            contract=contract,
            provider=provider,
            visibility=visibility,
        )

    def get(
        self,
        namespace: str,
        contract: type[Any],
    ) -> DependencyDescriptor:
        """
        Get dependency descriptor.

        Returns:
            DependencyDescriptor

        Raises:
            DependencyNotFoundError

        """
        try:
            return self._namespaces[namespace][contract]

        except KeyError as error:
            msg = f"{contract.__name__} not found in namespace '{namespace}'"
            raise DependencyNotFoundError(msg) from error

    def contains(
        self,
        namespace: str,
        contract: type[Any],
    ) -> bool:
        """
        Check dependency existence.

        Returns:
            bool

        """
        return (
            namespace in self._namespaces
            and contract in self._namespaces[namespace]
        )

    @property
    def namespaces(self) -> tuple[str, ...]:
        """
        Registered namespaces.

        Returns:
            tuple[str, ...]

        """
        return tuple(self._namespaces.keys())

    def snapshot(self) -> DependencyGraph:
        """
        Create graph snapshot.

        Returns:
            DependencyGraph

        """
        nodes: list[DependencyNode] = []

        for namespace, bucket in self._namespaces.items():
            nodes.extend(
                DependencyNode(
                    namespace=namespace,
                    contract=descriptor.contract.__name__,
                    provider=type(
                        descriptor.provider,
                    ).__name__,
                    scope=descriptor.provider.scope.value,
                    visibility=descriptor.visibility,
                )
                for descriptor in bucket.values()
            )

        return DependencyGraph(nodes=tuple(nodes))

    def snapshot(self) -> ContainerSnapshot:

        nodes: list[DependencyNode] = [
            DependencyNode(
                contract=descriptor.contract.__name__,
                namespace=descriptor.namespace.value,
                scope=descriptor.provider.scope.value,
                visibility=descriptor.visibility.value,
            )
            for descriptor in self._registry.descriptors
        ]

        return ContainerSnapshot(
            nodes=tuple(nodes),
        )
