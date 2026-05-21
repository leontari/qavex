"""Abstractions existing while kernel is running."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.infrastructure.registry import (
        InfrastructureRegistry,
    )
    from template_app.bootstrap.kernel.container import Container
    from template_app.bootstrap.lifecycle.manager import (
        LifecycleManager,
    )
    from template_app.bootstrap.lifecycle.registry import (
        LifecycleRegistry,
    )
    from template_app.bootstrap.messaging.runtime.command_bus import (
        RuntimeCommandBus,
    )
    from template_app.bootstrap.messaging.runtime.event_bus import (
        RuntimeEventBus,
    )
    from template_app.bootstrap.messaging.runtime.query_bus import (
        RuntimeQueryBus,
    )
    from template_app.bootstrap.messaging.runtime.registry import (
        RuntimeHandlerRegistry,
    )


@dataclass(slots=True)
class RuntimeState:
    """Application runtime state."""

    container: Container

    lifecycle_registry: LifecycleRegistry

    lifecycle_manager: LifecycleManager

    infrastructure_registry: InfrastructureRegistry

    messaging_registry: RuntimeHandlerRegistry

    event_bus: RuntimeEventBus

    command_bus: RuntimeCommandBus

    query_bus: RuntimeQueryBus
