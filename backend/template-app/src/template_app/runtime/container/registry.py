"""Dependency metadata registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)

if TYPE_CHECKING:
    from .contracts import DependencyProvider
    from .keys import DependencyKey
    from .namespace import Namespace
    from .types import DependencyVisibility


@dataclass(slots=True, frozen=True)
class DependencyDescriptor:
    """Immutable dependency metadata."""

    contract: type[Any]
    provider: DependencyProvider[Any]

    namespace: Namespace
    visibility: DependencyVisibility


@dataclass(slots=True)
class DependencyRegistry:
    """
    Metadata storage.

    Registry does NOT:
        - resolve dependencies
        - manage scopes
        - create instances
        - build graph

    Registry stores metadata only.
    """

    _descriptors: dict[DependencyKey, DependencyDescriptor] = field(
        default_factory=dict,
    )

    def register(
        self,
        descriptor: DependencyDescriptor,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register dependency metadata.

        Raises:
            DependencyAlreadyRegisteredError

        """
        key = DependencyKey(
            namespace=descriptor.namespace,
            contract=descriptor.contract,
        )

        if key in self._descriptors and not overwrite:
            msg = f"{descriptor.contract.__name__}"
            raise DependencyAlreadyRegisteredError(msg)

        self._descriptors[key] = descriptor

    def get(self, contract: type[Any]) -> DependencyDescriptor:
        """
        Get descriptor by contract.

        Returns:
            DependencyDescriptor

        Raises:
            DependencyNotFoundError

        """
        try:
            return self._descriptors[contract]

        except KeyError as error:
            raise DependencyNotFoundError(contract.__name__) from error

    def contains(self, contract: type[Any]) -> bool:
        """
        Check dependency registration.

        Returns:
            True if dependency descriptor is registered.

        """
        return contract in self._descriptors

    @property
    def namespaces(self) -> tuple[str, ...]:
        """
        Registered namespaces.

        Returns:
            tuple[str, ...]

        """
        return tuple(
            sorted({
                descriptor.namespace.name
                for descriptor in self._descriptors.values()
            })
        )

    @property
    def descriptors(self) -> tuple[DependencyDescriptor, ...]:
        """Return immutable metadata view."""
        return tuple(self._descriptors.values())

    def clear(self) -> None:
        """Testing helper."""
        self._descriptors.clear()
