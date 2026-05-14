"""
Runtime event system.

Provides:

- async event bus
- runtime event models
- dispatching
- event subscribers
- runtime event emission
"""

from __future__ import annotations

from template_app.platform.events.bus import (
    RuntimeEventBus,
)
from template_app.platform.events.dispatcher import (
    EventDispatcher,
)
from template_app.platform.events.emitter import (
    RuntimeEventEmitter,
)
from template_app.platform.events.event_types import (
    RuntimeEventType,
)
from template_app.platform.events.models import (
    RuntimeEvent,
)

__all__ = [
    "RuntimeEventBus",
    "EventDispatcher",
    "RuntimeEventEmitter",
    "RuntimeEventType",
    "RuntimeEvent",
]
