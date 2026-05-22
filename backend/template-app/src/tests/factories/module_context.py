from __future__ import annotations

from template_app.bootstrap.modules import (
    ModuleSetupContext,
)
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from tests.factories.apis import (
    build_infra_api,
    build_messaging_api,
    build_runtime_api,
)


def build_module_context(
    capabilities: frozenset[ModuleCapability] | None = None,
) -> ModuleSetupContext:

    return ModuleSetupContext(
        runtime=build_runtime_api(),
        infra=build_infra_api(),
        messaging=build_messaging_api(),
        capabilities=capabilities or frozenset(),
    )
