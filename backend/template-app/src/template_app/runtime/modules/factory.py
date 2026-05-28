from __future__ import annotations

from collections.abc import Iterable

from template_app.runtime.container.container import (
    Container,
)

from template_app.runtime.infrastructure.infra.cache.provider import (
    CacheProvider,
)
from template_app.runtime.infrastructure.infra.database.provider import (
    DatabaseProvider,
)
from template_app.runtime.infrastructure.infra.queue.provider import (
    QueueProvider,
)
from template_app.runtime.infrastructure.runtime import (
    InfrastructureRuntime,
)

from template_app.runtime.lifecycle.registry import (
    LifecycleRegistry,
)

from template_app.runtime.messaging.buses.command_bus import (
    RuntimeCommandBus,
)
from template_app.runtime.messaging.buses.event_bus import (
    RuntimeEventBus,
)
from template_app.runtime.messaging.buses.query_bus import (
    RuntimeQueryBus,
)
from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)

from template_app.runtime.modules import (
    ModuleCapability,
    ModuleContext,
)

from template_app.runtime.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)


def build_module_context(
    capabilities: Iterable[ModuleCapability] | None = None,
) -> ModuleContext:
    """
    Build isolated testing module context.

    Responsibilities:
        - runtime API isolation
        - messaging API isolation
        - infrastructure API isolation
        - capability testing support

    Returns:
        Initialized module context.
    """

    resolved_capabilities = frozenset(
        capabilities
        or {
            ModuleCapability.ROUTER,
            ModuleCapability.DEPENDENCIES,
            ModuleCapability.EVENT_BUS,
            ModuleCapability.INFRASTRUCTURE,
            ModuleCapability.LIFECYCLE,
        },
    )

    #
    # runtime api
    #

    runtime_api = ModuleRuntimeAPI(
        container=Container(),
        lifecycle_registry=LifecycleRegistry(),
    )

    #
    # infrastructure api
    #

    infrastructure_runtime = InfrastructureRuntime(
        cache=CacheProvider(
            url="redis://localhost:6379",
        ),
        database=DatabaseProvider(
            dsn="postgresql://localhost/test",
        ),
        queue=QueueProvider(
            brokers=["localhost:9092"],
        ),
    )

    infra_api = ModuleInfraAPI(
        runtime=infrastructure_runtime,
    )

    #
    # messaging api
    #

    handler_registry = RuntimeHandlerRegistry()

    messaging_api = ModuleMessagingAPI(
        event_bus=RuntimeEventBus(
            registry=handler_registry,
        ),
        command_bus=RuntimeCommandBus(
            registry=handler_registry,
        ),
        query_bus=RuntimeQueryBus(
            registry=handler_registry,
        ),
    )

    return ModuleContext(
        runtime=runtime_api,
        infra=infra_api,
        messaging=messaging_api,
        capabilities=resolved_capabilities,
    )
