"""Messaging runtime domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.messaging.buses import (
        RuntimeCommandBus,
        RuntimeEventBus,
        RuntimeQueryBus,
    )
    from template_app.runtime.messaging.registry import (
        RuntimeHandlerRegistry,
    )


@dataclass(slots=True)
class MessagingRuntime:
    """
    Messaging runtime domain.

    Responsibilities:
        - message bus ownership
        - handler registry ownership
    """

    registry: RuntimeHandlerRegistry

    event_bus: RuntimeEventBus

    command_bus: RuntimeCommandBus

    query_bus: RuntimeQueryBus
