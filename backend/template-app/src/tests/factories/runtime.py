from __future__ import annotations

from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.lifecycle.manager import LifecycleManager
from template_app.bootstrap.lifecycle.registry import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState
from tests.factories.events import build_event_bus
from tests.factories.infrastructure import build_infrastructure_registry

def build_runtime_state() -> RuntimeState:
    """Build runtime state."""

    lifecycle_registry = LifecycleRegistry()

    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    return RuntimeState(
        container=Container(),
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=(build_infrastructure_registry()),
        event_bus=build_event_bus(),
    )
