"""Public models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DependencyScope(StrEnum):
    """Dependency lifetime policy."""

    TRANSIENT = "transient"  # new object every time when called
    SINGLETON = "singleton"  # single object for the whole app
    SCOPED = "scoped"  # single object for a pipeline, then destroy


class DependencyVisibility(StrEnum):
    """Dependency visibility policy."""

    PUBLIC = "public"  # available to all
    PRIVATE = "private"  # available only for namespace members
    PROTECTED = "protected"


@dataclass(frozen=True, slots=True)
class Namespace:
    """
    Logical namespace.

    Used to define fine-grained separation inside system namespaces.

    Example:
        - Namespace("plugin.auth")
        - Namespace("transport.grpc")
        - Namespace("infra.redis")
        - kernel
        - plugin.auth
        - transport.grpc
        - infra.redis

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

    @classmethod
    def parse(cls, value: str | Namespace) -> Namespace:
        if isinstance(value, Namespace):
            return value

        return cls(value)

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

    def child(self, name: str) -> Namespace:
        return Namespace(f"{self.name}.{name}")

    def __str__(self) -> str:
        return self.name


class Namespaces:
    """
    Reserved root namespaces.

    These categories are top-level runtime boundaries used by Kernel
    for isolation, visibility and plugin separation.

    """

    KERNEL = Namespace("kernel")
    INFRA = Namespace("infra")
    TRANSPORT = Namespace("transport")
    MODULE = Namespace("module")
    PLUGIN = Namespace("plugin")
    GUI = Namespace("gui")
    TESTING = Namespace("testing")
    INTERNAL = Namespace("internal")

    @staticmethod
    def plugin(name: str) -> Namespace:
        return Namespace(f"plugin.{name}")

    @staticmethod
    def transport(name: str) -> Namespace:
        return Namespace(f"transport.{name}")

    @staticmethod
    def infra(name: str) -> Namespace:
        return Namespace(f"infra.{name}")
