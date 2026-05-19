from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from template_app.bootstrap.integration.models import IntegrationEvent


class IntegrationEventHandler(Protocol):
    async def __call__(self, event: IntegrationEvent) -> None: ...
