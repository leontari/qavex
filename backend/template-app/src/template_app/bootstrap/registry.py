from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from template_app.bootstrap.contracts import ModuleProtocol


class ModuleRegistry:
    """
    Dynamic runtime module registry.

    Responsible for:

    - module registration
    - module discovery
    - deterministic load ordering
    - runtime module iteration
    """

    def __init__(self) -> None:
        self._modules: list[ModuleProtocol] = []

    def register(self, module: ModuleProtocol) -> None:
        """Register application module."""
        self._modules.append(module)

    def extend(self, modules: Iterable[ModuleProtocol]) -> None:
        """Register multiple modules."""
        self._modules.extend(modules)

    @property
    def modules(self) -> tuple[ModuleProtocol, ...]:
        """Return immutable module collection."""
        return tuple(self._modules)
