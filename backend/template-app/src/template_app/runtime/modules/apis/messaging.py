from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.messaging.buses.command_bus import (
        RuntimeCommandBus,
    )
    from template_app.runtime.messaging.buses.event_bus import (
        RuntimeEventBus,
    )
    from template_app.runtime.messaging.buses.query_bus import (
        RuntimeQueryBus,
    )


@dataclass(slots=True)
class ModuleMessagingAPI:
    """Restricted messaging API."""

    event_bus: RuntimeEventBus
    command_bus: RuntimeCommandBus
    query_bus: RuntimeQueryBus
