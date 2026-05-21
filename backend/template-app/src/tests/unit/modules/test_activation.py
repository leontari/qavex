from template_app.bootstrap.modules.activation import (
    activate_module,
)
from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from template_app.bootstrap.modules.context import (
    ModuleSetupContext,
)
from template_app.bootstrap.modules.manifest import (
    ModuleManifest,
)
from tests.factories.kernel import (
    build_testing_kernel,
)


class FakeModule:

    def __init__(self) -> None:
        self.loaded = False

    def setup(self, context) -> None:
        self.loaded = True


def test_activate_module() -> None:

    kernel = build_testing_kernel()

    module = FakeModule()

    manifest = ModuleManifest(
        name="fake",
        module=module,
        capabilities=frozenset({
            ModuleCapability.ROUTER,
        }),
    )

    context = ModuleSetupContext(
        runtime=kernel.runtime_api,
        infra=kernel.infra_api,
        messaging=kernel.messaging_api,
        capabilities=manifest.capabilities,
    )

    activate_module(
        manifest=manifest,
        context=context,
    )

    assert module.loaded is True
