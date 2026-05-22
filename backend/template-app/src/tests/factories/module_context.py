from __future__ import annotations

from collections.abc import Iterable

from fastapi import FastAPI

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.kernel import Container
from template_app.bootstrap.lifecycle import (
    LifecycleManager,
    LifecycleRegistry,
)
from template_app.bootstrap.messaging.runtime import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeHandlerRegistry,
    RuntimeQueryBus,
)
from template_app.bootstrap.modules import (
    ModuleCapability,
    ModuleSetupContext,
)
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)


def build_module_context(
    capabilities: Iterable[ModuleCapability] | None = None,
) -> ModuleSetupContext:

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

    return ModuleSetupContext(
        runtime=runtime_api,
        infra=infra_api,
        messaging=messaging_api,
        capabilities=frozenset(capabilities),
    )
