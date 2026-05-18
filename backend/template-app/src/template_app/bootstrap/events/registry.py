from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.events.protocols import EventHandler


@dataclass(slots=True)
class EventRegistry:
    """Runtime event registry."""

    _handlers: dict[str, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
    )

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._handlers[event_name].append(handler)

    def get_handlers(self, event_name: str) -> tuple[EventHandler, ...]:
        return tuple(self._handlers[event_name])
