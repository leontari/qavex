# keys.py

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.container.namespace import Namespace


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
