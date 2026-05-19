from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.integration.models import (
        IntegrationEvent,
    )
    from template_app.bootstrap.integration.registry import (
        IntegrationHandlerRegistry,
    )


@dataclass(slots=True)
class RuntimeIntegrationBus:
    """In-memory runtime integration bus."""

    registry: IntegrationHandlerRegistry

    async def publish(
        self,
        event: IntegrationEvent,
    ) -> None:

        handlers = self.registry.get_handlers(type(event))

        for handler in handlers:
            await handler(event)
