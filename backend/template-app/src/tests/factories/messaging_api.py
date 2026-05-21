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
    ModuleMessagingAPI,
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
