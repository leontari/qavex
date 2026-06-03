from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FakeQueryBus:
    """
    Fake query bus for testing.
    """

    executed: list[Any] = field(default_factory=list)

    response: Any = None

    async def execute(
        self,
        query: Any,
    ) -> Any:

        self.executed.append(query)

        return self.response
