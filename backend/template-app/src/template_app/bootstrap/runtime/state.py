"""RuntimeState."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.events.bus import EventBus
    from template_app.bootstrap.infrastructure.registry import (
        InfrastructureRegistry,
    )
    from template_app.bootstrap.kernel import Container
    from template_app.bootstrap.lifecycle.manager import LifecycleManager
    from template_app.bootstrap.lifecycle.registry import LifecycleRegistry
    from template_app.bootstrap.messaging.buses import (
        CommandBus,
        QueryBus,
    )
    from template_app.bootstrap.messaging.registry import (
        MessageHandlerRegistry,
    )


@dataclass(slots=True)
class RuntimeState:
    """Application runtime state."""

    container: Container

    infrastructure_registry: InfrastructureRegistry

    lifecycle_registry: LifecycleRegistry
    lifecycle_manager: LifecycleManager

    event_bus: EventBus

    message_registry: MessageHandlerRegistry
    command_bus: CommandBus
    query_bus: QueryBus
