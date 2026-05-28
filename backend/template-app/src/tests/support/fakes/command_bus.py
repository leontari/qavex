from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FakeCommandBus:
    """
    Fake command bus for testing.
    """

    dispatched: list[Any] = field(default_factory=list)

    async def dispatch(
        self,
        command: Any,
    ) -> None:

        self.dispatched.append(command)
