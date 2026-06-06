from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .diagnostics import ContainerSnapshot
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
    """
    Registered dependency descriptor.

    Stores metadata only.

    Lifecycle is managed by DependencyManager.
    """

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
        - diagnostics snapshot creation

    No resolve logic is allowed here.

    Does NOT:
        - resolve dependencies
        - create instances
        - manage lifecycle
        - manage scopes
    """

    # _namespaces: dict[str, dict[type[Any], DependencyDescriptor]] = field(
    #     default_factory=dict,
    # )

    _descriptors: dict[tuple[str, type[Any]], DependencyDescriptor] = field(
        default_factory=dict,
    )

    def register(
        self,
        namespace: Namespace,
        contract: type[Any],
        provider: DependencyProvider,
        visibility: DependencyVisibility,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency metadata.

        Args:
            namespace:
                Dependency namespace name.

            contract:
                Dependency contract.

            provider:
                Provider instance.

            visibility:
                Visibility policy.

            overwrite:
                Allow to overwrite.

        Raises:
            DependencyAlreadyRegisteredError

        """
        # bucket = self._namespaces.setdefault(namespace, {})
        key = (namespace.name, contract)

        if key in self._descriptors and not overwrite:
            msg = (
                f"{contract.__name__} already registered in '{namespace.name}'"
            )
            raise DependencyAlreadyRegisteredError(msg)

        # bucket[contract] = DependencyDescriptor(
        #     contract=contract,
        #     provider=provider,
        #     visibility=visibility,
        # )
        self._descriptors[key] = DependencyDescriptor(
            contract=contract,
            provider=provider,
            namespace=namespace,
            visibility=visibility,
        )

    # def get(
    #     self,
    #     namespace: str,
    #     contract: type[Any],
    # ) -> DependencyDescriptor:
    #     """
    #     Get dependency descriptor.
    #
    #     Returns:
    #         DependencyDescriptor
    #
    #     Raises:
    #         DependencyNotFoundError
    #
    #     """
    #     try:
    #         return self._namespaces[namespace][contract]
    #
    #     except KeyError as error:
    #         msg = f"{contract.__name__} not found in namespace '{namespace}'"
    #         raise DependencyNotFoundError(msg) from error

    def find(self, contract: type[Any]) -> DependencyDescriptor:
        """
        Find descriptor by contract.

        Returns:
            DependencyDescriptor

        Raises:
            DependencyNotFoundError

        """
        for descriptor in self._descriptors.values():
            if descriptor.contract is contract:
                return descriptor

        msg = f"Dependency not registered: {contract.__name__}"
        raise DependencyNotFoundError(msg)

    def contains(
        self,
        # namespace: str,
        contract: type[Any],
    ) -> bool:
        """
        Check dependency existence.

        Returns:
            bool

        """
        try:
            self.find(contract)
            return True
        except DependencyNotFoundError:
            return False

        # return (
        #     namespace in self._namespaces
        #     and contract in self._namespaces[namespace]
        # )

    @property
    def namespaces(self) -> tuple[str, ...]:
        """
        Registered namespaces.

        Returns:
            tuple[str, ...]

        """
        # return tuple(self._namespaces.keys())
        return tuple(
            sorted({
                descriptor.namespace.name
                for descriptor in self._descriptors.values()
            })
        )

    def snapshot(self) -> ContainerSnapshot:
        """
        Create diagnostics graph snapshot.

        Returns:
            ContainerSnapshot

        """
        # nodes: list[DependencyNode] = []
        #
        # for namespace, bucket in self._namespaces.items():
        #     nodes.extend(
        #         DependencyNode(
        #             namespace=namespace,
        #             contract=descriptor.contract.__name__,
        #             provider=type(
        #                 descriptor.provider,
        #             ).__name__,
        #             scope=descriptor.provider.scope.value,
        #             visibility=descriptor.visibility,
        #         )
        #         for descriptor in bucket.values()
        #     )
        #
        # return DependencyGraph(nodes=tuple(nodes))
        nodes = tuple(
            DependencyNode(
                namespace=descriptor.namespace.name,
                contract=descriptor.contract.__name__,
                provider=type(descriptor.provider.__name__),
                scope=descriptor.provider.scope.value,
                visibility=descriptor.visibility.value,
            )
            for descriptor in self._descriptors.values()
        )
        return ContainerSnapshot(nodes=nodes)
