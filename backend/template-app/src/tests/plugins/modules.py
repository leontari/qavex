from __future__ import annotations

from collections.abc import Iterable

import pytest

from template_app.runtime.modules.context import (
    ModuleContext,
)

from template_app.runtime.modules.capabilities import (
    ModuleCapability,
)

from template_app.runtime.modules.apis.runtime import (
    ModuleRuntimeAPI,
)

from template_app.runtime.modules.apis.infrastructure import (
    ModuleInfraAPI,
)

from template_app.runtime.modules.apis.messaging import (
    ModuleMessagingAPI,
)

from template_app.runtime.kernel.runtime.state import (
    RuntimeState,
)


@pytest.fixture
def module_capabilities() -> frozenset[ModuleCapability]:
    return frozenset(
        {
            ModuleCapability.ROUTER,
            ModuleCapability.DEPENDENCIES,
            ModuleCapability.EVENT_BUS,
            ModuleCapability.INFRASTRUCTURE,
            ModuleCapability.LIFECYCLE,
        }
    )


@pytest.fixture
def module_context(
    runtime_state: RuntimeState,
    module_capabilities: Iterable[ModuleCapability],
) -> ModuleContext:

    return ModuleContext(
        runtime=ModuleRuntimeAPI(
            container=runtime_state.container,
            lifecycle_registry=runtime_state.lifecycle.registry,
        ),
        infra=ModuleInfraAPI(
            registry=runtime_state.infrastructure.registry,
        ),
        messaging=ModuleMessagingAPI(
            event_bus=runtime_state.messaging.event_bus,
            command_bus=runtime_state.messaging.command_bus,
            query_bus=runtime_state.messaging.query_bus,
        ),
        capabilities=frozenset(module_capabilities),
    )
