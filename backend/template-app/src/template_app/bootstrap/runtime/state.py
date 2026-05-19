"""RuntimeState."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.commands.dispatcher import (
        CommandDispatcher,
    )
    from template_app.bootstrap.dispatching.queries.dispatcher import (
        QueryDispatcher,
    )
    from template_app.bootstrap.dispatching.registry import (
        MessageHandlerRegistry,
    )
    from template_app.bootstrap.infrastructure.registry import (
        InfrastructureRegistry,
    )
    from template_app.bootstrap.integration.bus import (
        RuntimeIntegrationBus,
    )
    from template_app.bootstrap.integration.registry import (
        IntegrationHandlerRegistry,
    )
    from template_app.bootstrap.kernel.container import Container
    from template_app.bootstrap.lifecycle.manager import (
        LifecycleManager,
    )
    from template_app.bootstrap.lifecycle.registry import (
        LifecycleRegistry,
    )


@dataclass(slots=True)
class RuntimeState:
    """Application runtime state."""

    container: Container

    lifecycle_registry: LifecycleRegistry

    lifecycle_manager: LifecycleManager

    infrastructure_registry: InfrastructureRegistry

    integration_registry: IntegrationHandlerRegistry

    integration_bus: RuntimeIntegrationBus

    message_registry: MessageHandlerRegistry

    command_dispatcher: CommandDispatcher

    query_dispatcher: QueryDispatcher
