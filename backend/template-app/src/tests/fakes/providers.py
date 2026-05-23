from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from template_app.runtime.container.contracts import (
    DependencyProvider,
)


@dataclass(slots=True)
class FakeDependencyProvider(DependencyProvider):
    """
    Fake DI provider.
    """

    value: Any

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> str:
        return "singleton"

    def provide(self) -> Any:
        return self.value
