from __future__ import annotations

from collections.abc import Iterable

import pytest

from template_app.runtime.modules.context import (
    ModuleContext,
)
from template_app.runtime.modules.capabilities import (
    ModuleCapability,
)
from template_app.runtime.modules.manifests import (
    ModuleManifest,
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


@pytest.fixture
def module_capabilities() -> frozenset[ModuleCapability]:
    return frozenset(
        {
            ModuleCapability.ROUTER,
            ModuleCapability.DEPENDENCIES,
            ModuleCapability.EVENT_BUS,
            ModuleCapability.INFRASTRUCTURE,
            ModuleCapability.LIFECYCLE,
        },
    )


@pytest.fixture
def module_context(
    runtime,
    module_capabilities: Iterable[ModuleCapability],
) -> ModuleContext:
    """
    Restricted module runtime context.
    """

    return ModuleContext(
        runtime=ModuleRuntimeAPI(
            container=runtime.container,
            lifecycle_registry=runtime.lifecycle.registry,
        ),
        infra=ModuleInfraAPI(
            registry=runtime.infrastructure.registry,
        ),
        messaging=ModuleMessagingAPI(
            event_bus=runtime.messaging.event_bus,
            command_bus=runtime.messaging.command_bus,
            query_bus=runtime.messaging.query_bus,
        ),
        capabilities=frozenset(
            module_capabilities,
        ),
    )


@pytest.fixture
def module_registry(runtime):
    return runtime.modules.registry


@pytest.fixture
def fake_module_manifest() -> ModuleManifest:
    return ModuleManifest(
        name="test-module",
        description="test module",
    )
