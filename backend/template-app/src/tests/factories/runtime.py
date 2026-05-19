from __future__ import annotations

from template_app.bootstrap.dispatching.commands.dispatcher import CommandDispatcher
from template_app.bootstrap.dispatching.queries.dispatcher import QueryDispatcher
from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.integration.bus import RuntimeIntegrationBus
from template_app.bootstrap.integration.registry import IntegrationHandlerRegistry
from template_app.bootstrap.kernel.container import Container
from template_app.bootstrap.lifecycle.manager import LifecycleManager
from template_app.bootstrap.lifecycle.registry import LifecycleRegistry
from template_app.bootstrap.dispatching.registry import MessageHandlerRegistry
from template_app.bootstrap.runtime.state import RuntimeState


def build_runtime_state() -> RuntimeState:
    """
    Build runtime state.

    Returns:
        RuntimeState: pure runtime
    """
    lifecycle_registry = LifecycleRegistry()

    message_registry = MessageHandlerRegistry()

    integration_registry = IntegrationHandlerRegistry()

    return RuntimeState(
        container=Container(),
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=LifecycleManager(registry=lifecycle_registry),
        infrastructure_registry=InfrastructureRegistry(),
        integration_registry=integration_registry,
        integration_bus=RuntimeIntegrationBus(registry=integration_registry),
        message_registry=message_registry,
        command_dispatcher=CommandDispatcher(registry=message_registry),
        query_dispatcher=QueryDispatcher(registry=message_registry)
    )
