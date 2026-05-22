from fastapi import FastAPI

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.messaging.runtime import (
    RuntimeCommandBus,
    RuntimeEventBus,
    RuntimeQueryBus,
    RuntimeHandlerRegistry,
)
from template_app.bootstrap.modules.apis import (
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
    ModuleInfraAPI,
)
from template_app.bootstrap.kernel import (
    Container,
)
from template_app.bootstrap.lifecycle import (
    LifecycleRegistry,
)


def build_infra_api() -> ModuleInfraAPI:

    return ModuleInfraAPI(
        registry=InfrastructureRegistry(),
    )


def build_messaging_api() -> ModuleMessagingAPI:

    registry = RuntimeHandlerRegistry()

    return ModuleMessagingAPI(
        event_bus=RuntimeEventBus(
            registry=registry,
        ),
        command_bus=RuntimeCommandBus(
            registry=registry,
        ),
        query_bus=RuntimeQueryBus(
            registry=registry,
        ),
    )

def build_runtime_api() -> ModuleRuntimeAPI:

    return ModuleRuntimeAPI(
        app=FastAPI(),
        container=Container(),
        lifecycle_registry=LifecycleRegistry(),
    )
