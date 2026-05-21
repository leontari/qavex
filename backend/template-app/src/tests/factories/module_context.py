from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from template_app.bootstrap.modules.context import (
    ModuleSetupContext,
)

from tests.factories.infra_api import (
    build_infra_api,
)
from tests.factories.messaging_api import (
    build_messaging_api,
)
from tests.factories.runtime_api import (
    build_runtime_api,
)


def build_module_context(
    capabilities: frozenset[ModuleCapability],
) -> ModuleSetupContext:

    return ModuleSetupContext(
        runtime=build_runtime_api(),
        infra=build_infra_api(),
        messaging=build_messaging_api(),
        capabilities=capabilities,
    )
