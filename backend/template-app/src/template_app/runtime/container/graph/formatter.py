from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyId


class DependencyGraphFormatter:
    """Graph helpers."""

    @staticmethod
    def node_id(dep: DependencyId) -> str:
        """
        Graph identifier.

        Example:
            plugin.auth:app.services.UserService

        Returns:
            string identifier

        """
        return (
            f"{dep.namespace.name}:"
            f"{dep.contract.__module__}."
            f"{dep.contract.__qualname__}"
        )
