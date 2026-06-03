from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from template_app.runtime.container.contracts import (
    DependencyProvider,
)


@dataclass(slots=True)
class FakeDependencyProvider(DependencyProvider):
    """
    Generic infrastructure provider fake.
    """

    initialized: bool = False

    shutdown_called: bool = False

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> str:
        return "singleton"

    async def startup(self) -> None:
        self.initialized = True

    async def shutdown(self) -> None:
        self.shutdown_called = True
