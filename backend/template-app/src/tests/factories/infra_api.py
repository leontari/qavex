from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
)


def build_infra_api() -> ModuleInfraAPI:

    return ModuleInfraAPI(
        registry=InfrastructureRegistry(),
    )
