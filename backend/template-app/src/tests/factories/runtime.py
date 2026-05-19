from __future__ import annotations

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.lifecycle.manager import LifecycleManager
from template_app.bootstrap.lifecycle.registry import LifecycleRegistry
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
from template_app.bootstrap.runtime.state import RuntimeState


def build_runtime_state() -> RuntimeState:
    """
    Build runtime state.

    Returns:
        RuntimeState: pure runtime
    """
    container = Container()

    lifecycle_registry = LifecycleRegistry()
    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    infrastructure_registry = InfrastructureRegistry()

    messaging_registry = RuntimeHandlerRegistry()
    event_bus = RuntimeEventBus(registry=messaging_registry)
    command_bus = RuntimeCommandBus(registry=messaging_registry)
    query_bus = RuntimeQueryBus(registry=messaging_registry)

    return RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=infrastructure_registry,
        messaging_registry=messaging_registry,
        event_bus=event_bus,
        command_bus=command_bus,
        query_bus=query_bus,
    )
