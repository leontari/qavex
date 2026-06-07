from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .diagnostics import ContainerSnapshot
from .exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)
from .graph import DependencyNode

if TYPE_CHECKING:
    from .contracts import DependencyProvider
    from .namespace import Namespace
    from .types import DependencyVisibility


@dataclass(slots=True, frozen=True)
class DependencyDescriptor:
    """Immutable dependency registration metadata."""

    contract: type[Any]
    provider: DependencyProvider[Any]
    namespace: Namespace
    visibility: DependencyVisibility


@dataclass(slots=True)
class DependencyRegistry:
    """
    Global dependency metadata registry.

    Responsibilities:
        - store dependency descriptors
        - ensure uniqueness of contracts
        - provide lookup by contract
        - provide diagnostics snapshot

    No resolve logic is allowed here.

    Explicitly does NOT:
        - resolve dependencies
        - enforce visibility
        - manage lifecycle
        - manage scopes
    """

    # _store: dict[tuple[str, type[Any]], DependencyDescriptor] = field(
    #     default_factory=dict,
    # )
    _descriptors: dict[type[Any], DependencyDescriptor] = field(
        default_factory=dict,
    )

    def register(
        self,
        # namespace: Namespace,
        # contract: type[Any],
        # provider: DependencyProvider[Any],
        # visibility: DependencyVisibility,
        descriptor: DependencyDescriptor,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency metadata.

        Args:
            namespace: ownership namespace
            contract: dependency contract type
            provider: provider implementation
            visibility: access policy
            overwrite: allow to overwrite existing registration

        Raises:
            DependencyAlreadyRegisteredError

        """
        # key = (namespace.name, contract)
        #
        # if key in self._store and not overwrite:
        #     msg = (
        #         f"{contract.__name__} already registered in '{namespace.name}'"
        #     )
        #     raise DependencyAlreadyRegisteredError(msg)
        #
        # self._store[key] = DependencyDescriptor(
        #     contract=contract,
        #     provider=provider,
        #     namespace=namespace,
        #     visibility=visibility,
        # )

        contract = descriptor.contract

        if contract in self._descriptors and overwrite:
            raise DependencyAlreadyRegisteredError(contract.__name__)

        self._descriptors[contract] = descriptor

    def get(
        self,
        # namespace: Namespace,
        contract: type[Any],
    ) -> DependencyDescriptor:
        """
        Find descriptor by namespace and contract.

        Returns:
            DependencyDescriptor

        Raises:
            DependencyNotFoundError

        """
        # key = (namespace.name, contract)
        #
        # try:
        #     return self._store[key]
        # except KeyError as error:
        #     msg = (
        #         f"{contract.__name__} "
        #         f"not registered in namespace "
        #         f"'{namespace.name}'"
        #     )
        #     raise DependencyNotFoundError(msg) from error
        try:
            return self._descriptors[contract]
        except KeyError as error:
            raise DependencyNotFoundError(contract.__name__) from error

    def contains(
        self,
        # namespace: Namespace,
        contract: type[Any],
    ) -> bool:
        """
        Check dependency existence.

        Returns:
            bool

        """
        # return (namespace.name, contract) in self._container
        return contract in self._descriptors

    # @property
    # def namespaces(self) -> tuple[str, ...]:
    #     """
    #     Registered namespaces.
    #
    #     Returns:
    #         tuple[str, ...]
    #
    #     """
    #     return tuple(
    #         sorted({
    #             descriptor.namespace.name
    #             for descriptor in self._container.values()
    #         })
    #     )
    #
    # def snapshot(self) -> ContainerSnapshot:
    #     """
    #     Create diagnostics graph snapshot.
    #
    #     Returns:
    #         ContainerSnapshot
    #
    #     """
    #     nodes = tuple(
    #         DependencyNode(
    #             namespace=descriptor.namespace.name,
    #             contract=descriptor.contract.__name__,
    #             provider=type(descriptor.provider).__name__,
    #             scope=descriptor.provider.scope.value,
    #             visibility=descriptor.visibility.value,
    #         )
    #         for descriptor in self._store.values()
    #     )
    #     return ContainerSnapshot(nodes=nodes)
    #
    # def locate(
    #     self,
    #     contract: type[Any],
    # ) -> tuple[Namespace, DependencyDescriptor]:
    #
    #     for descriptor in self._store.values():
    #         if descriptor.contract is contract:
    #             return descriptor.namespace, descriptor
    #
    #     raise DependencyNotFoundError(contract.__name__)

    @property
    def descriptors(self) -> tuple[DependencyDescriptor, ...]:
        return tuple(self._descriptors.values())
