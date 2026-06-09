"""Dependency metadata registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from .exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)

if TYPE_CHECKING:
    from template_app.runtime.container.keys import DependencyKey
    from template_app.runtime.container.namespace import Namespace

    from .contracts import DependencyProvider
    from .types import DependencyVisibility


class DependencyNamespace(StrEnum):
    """
    Reserved root namespaces.

    These categories are top-level runtime boundaries used
    for isolation, visibility and plugin separation.

    """

    KERNEL = "kernel"
    INFRA = "infra"
    TRANSPORT = "transport"
    MODULE = "module"
    PLUGIN = "plugin"
    GUI = "gui"
    TESTING = "testing"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class Namespace:
    """
    Logical namespace.

    Used to define fine-grained separation inside system namespaces.

    Examples:
        Namespace("plugin.auth")
        Namespace("transport.grpc")
        Namespace("infra.redis")

    """

    name: str

    def __post_init__(self) -> None:
        """Validate namespace format."""
        if not self.name or not self.name.strip():
            msg = "Namespace name cannot be empty"
            raise ValueError(msg)

        if ".." in self.name:
            msg = f"Invalid namespace name format: {self.name}"
            raise ValueError(msg)

    @property
    def root(self) -> str:
        """
        Root segment of namespace.

        Example:
            "plugin.auth" -> "plugin"

        """
        return self.name.split(".")[0]

    @property
    def parts(self) -> tuple[str, ...]:
        """
        Split namespace into hierarchical segments.

        Example:
            "plugin.auth.jwt" -> ("plugin", "auth", "jwt")

        """
        return tuple(self.name.split("."))

    @property
    def is_plugin(self) -> bool:
        return self.root == DependencyNamespace.PLUGIN

    @property
    def is_kernel(self) -> bool:
        return self.name == DependencyNamespace.KERNEL

    def belongs_to(self, parent: Namespace) -> bool:
        """
        Hierarchical ownership check.

        plugin.auth.jwt
        belongs_to(plugin.auth)

        Returns:
            bool

        """
        return self.name == parent.name or self.name.startswith(
            f"{parent.name}"
        )

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class DependencyKey:
    """
    Unique dependency identifier.

    Identifies a dependency inside container runtime.
    """

    namespace: Namespace
    contract: type[Any]

    @property
    def node_id(self) -> str:
        """
        Stable graph identifier.

        Example:
            plugin.auth:app.services.UserService

        """
        return (
            f"{self.namespace.name}:"
            f"{self.contract.__module__}."
            f"{self.contract.__qualname__}"
        )

    def __str__(self) -> str:
        return self.node_id


@dataclass(slots=True, frozen=True)
class DependencyDescriptor:
    """Immutable dependency metadata."""

    provider: DependencyProvider[Any]
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

    _descriptors: dict[DependencyKey:DependencyDescriptor] = field(
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
