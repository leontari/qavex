from __future__ import annotations

from collections.abc import Iterable

from fastapi import FastAPI

from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.runtime.container.container import Container
from template_app.runtime.lifecycle import (
    LifecycleManager,
    LifecycleRegistry,
)
from template_app.runtime.messaging.runtime import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeHandlerRegistry,
    RuntimeQueryBus,
)
from template_app.runtime.module import (
    ModuleCapability,
    ModuleContext,
)
from template_app.runtime.module.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)


def build_module_context(
    capabilities: Iterable[ModuleCapability] | None = None,
) -> ModuleContext:

    capabilities = capabilities or frozenset({
        ModuleCapability.ROUTER,
        ModuleCapability.DEPENDENCIES,
        ModuleCapability.EVENT_BUS,
        ModuleCapability.INFRASTRUCTURE,
        ModuleCapability.LIFECYCLE,
    })

    container = Container()

    lifecycle_registry = LifecycleRegistry()

    lifecycle_manager = LifecycleManager(
        registry=lifecycle_registry,
    )

    messaging_registry = RuntimeHandlerRegistry()

    infrastructure_registry = InfrastructureRegistry()

    runtime_api = ModuleRuntimeAPI(
        app=FastAPI(),
        container=container,
        lifecycle_registry=lifecycle_registry,
    )

    infra_api = ModuleInfraAPI(
        registry=infrastructure_registry,
    )

    messaging_api = ModuleMessagingAPI(
        event_bus=RuntimeEventBus(
            registry=messaging_registry,
        ),
        command_bus=RuntimeCommandBus(
            registry=messaging_registry,
        ),
        query_bus=RuntimeQueryBus(
            registry=messaging_registry,
        ),
    )

    return ModuleContext(
        runtime=runtime_api,
        infra=infra_api,
        messaging=messaging_api,
        capabilities=frozenset(capabilities),
    )
