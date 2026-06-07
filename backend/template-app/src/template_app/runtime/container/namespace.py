"""Runtime dependency namespaces."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DependencyNamespace(StrEnum):
    """
    System-level pre-defined namespace categories.

    These categories are top-level runtime boundaries used by Kernel
    for isolation, visibility and plugin separation.

    """

    KERNEL = "kernel"
    INFRASTRUCTURE = "infrastructure"
    TRANSPORT = "transport"
    MODULE = "module"
    PLUGIN = "plugin"
    GUI = "gui"
    TESTING = "testing"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class Namespace:
    """
    Logical namespace instance.

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
            msg = "Invalid namespace format"
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """
        Split namespace into hierarchical segments.

        Example:
            "plugin.auth.jwt" -> ("plugin", "auth", "jwt")

        """
        return tuple(self.name.split("."))

    @property
    def root(self) -> str:
        """
        Root segment of namespace.

        Example:
            "plugin.auth" -> "plugin"

        """
        return self.parts[0]

    @property
    def is_plugin(self) -> bool:
        return self.root == "plugin"

    @classmethod
    def is_transport(self) -> bool:
        return self.root == "transport"

    @classmethod
    def is_infrastructure(self) -> bool:
        return self.root == "infra"

    @property
    def is_kernel(self) -> bool:
        return self.name == "kernel"

    def __str__(self) -> str:
        return self.name
