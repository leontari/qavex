from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Container:
    """
    Application Runtime DI Container.

    Container is used for:
    - runtime service registry;
    - application runtime dependency graph.

    Stores runtime services and infrastructure adapters.

    FastAPI DI and Runtime DI are separated from each other.
    FastAPI DI is used only as transport-layer dependency injection.
    """

    _dependencies: dict[str, Any] = field(default_factory=dict)

    def register(self, key: str, dependency: Any) -> None:
        """Register dependency."""

        self._dependencies[key] = dependency

    def resolve(self, key: str) -> Any:
        """Resolve dependency."""

        try:
            return self._dependencies[key]

        except KeyError as error:
            msg = f"Dependency '{key}' not found."
            raise LookupError(msg) from error

    def contains(self, key: str) -> bool:
        """Check dependency existence."""

        return key in self._dependencies

    @property
    def dependencies(self) -> dict[str, Any]:
        """Readonly dependency mapping."""

        return dict(self._dependencies)
