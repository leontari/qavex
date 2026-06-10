"""Runtime dependency namespaces."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DependencyNamespace(StrEnum):
    """
    Reserved root namespaces.

    These categories are top-level runtime boundaries used by Kernel
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

    Example:
        - Namespace("plugin.auth")
        - Namespace("transport.grpc")
        - Namespace("infra.redis")

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
