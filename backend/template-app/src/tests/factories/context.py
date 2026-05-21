from fastapi import FastAPI

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.kernel import (
    Container,
)
from template_app.bootstrap.lifecycle import (
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
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from template_app.bootstrap.modules.context import (
    ModuleSetupContext,
)


def build_module_context(
    capabilities: frozenset[ModuleCapability],
) -> ModuleSetupContext:

    app = FastAPI()

    container = Container()

    lifecycle_registry = LifecycleRegistry()

    messaging_registry = RuntimeHandlerRegistry()

    runtime_api = ModuleRuntimeAPI(
        app=app,
        container=container,
        lifecycle_registry=lifecycle_registry,
    )

    infra_api = ModuleInfraAPI(
        registry=InfrastructureRegistry(),
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
        capabilities=capabilities,
    )
