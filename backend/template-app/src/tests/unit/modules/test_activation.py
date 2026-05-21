from template_app.bootstrap.modules.activation import (
    activate_module,
)
from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from template_app.bootstrap.modules.manifests import (
    ModuleManifest,
)
from tests.factories.module_context import (
    build_module_context,
)


class FakeModule:

    def __init__(self) -> None:
        self.loaded = False

    def setup(self, context) -> None:
        self.loaded = True


def test_activate_module() -> None:

    module = FakeModule()

    manifest = ModuleManifest(
        name="fake",
        module=module,
        capabilities=frozenset({
            ModuleCapability.ROUTER,
        }),
    )

    context = build_module_context(
        manifest.capabilities,
    )

    activate_module(
        manifest=manifest,
        context=context,
    )

    assert module.loaded is True
