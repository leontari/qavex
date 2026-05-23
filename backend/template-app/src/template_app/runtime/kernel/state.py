"""Abstractions existing while kernel is running."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.container import Container
    from template_app.runtime.infrastructure.registry import (
        InfrastructureRegistry,
    )
    from template_app.runtime.lifecycle import (
        LifecycleManager,
        LifecycleRegistry,
    )
    from template_app.runtime.messaging.runtime import (
        RuntimeCommandBus,
        RuntimeEventBus,
        RuntimeQueryBus,
    )
    from template_app.runtime.messaging.runtime.registry import (
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
