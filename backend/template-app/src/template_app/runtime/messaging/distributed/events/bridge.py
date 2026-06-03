from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from template_app.runtime.messaging.contracts.events import Event


class DistributedEventBridge(Protocol):
    async def publish(self, event: Event) -> None: ...
