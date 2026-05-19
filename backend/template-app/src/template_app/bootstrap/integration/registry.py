from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.integration.models import (
        IntegrationEvent,
    )
    from template_app.bootstrap.integration.protocols import (
        IntegrationEventHandler,
    )


@dataclass(slots=True)
class IntegrationHandlerRegistry:
    """Runtime integration handler registry."""

    _handlers: dict[
        type[IntegrationEvent],
        list[IntegrationEventHandler],
    ] = field(
        default_factory=lambda: defaultdict(list),
    )

    def subscribe(
        self,
        event_type: type[IntegrationEvent],
        handler: IntegrationEventHandler,
    ) -> None:
        self._handlers[event_type].append(handler)

    def get_handlers(
        self,
        event_type: type[IntegrationEvent],
    ) -> tuple[IntegrationEventHandler, ...]:
        return tuple(self._handlers[event_type])
