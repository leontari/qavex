from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FakeEventBus:
    """
    Fake runtime event bus for testing.
    """

    published: list[Any] = field(default_factory=list)

    subscribers: dict[str, list[Any]] = field(
        default_factory=dict,
    )

    async def publish(
        self,
        event: Any,
    ) -> None:

        self.published.append(event)

    def subscribe(
        self,
        event_name: str,
        handler: Any,
    ) -> None:

        self.subscribers.setdefault(
            event_name,
            [],
        ).append(handler)
