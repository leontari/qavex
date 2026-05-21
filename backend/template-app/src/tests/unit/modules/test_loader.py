from template_app.bootstrap.modules import (
    ModuleSetupContext,
    ModuleManifest,
    load_modules,
)
from template_app.bootstrap.runtime import bootstrap_application


class FakeModule:

    loaded: bool = False

    def setup(self, context: ModuleSetupContext) -> None:
        self.loaded = True


def test_loader_executes_module_setup() -> None:
    kernel = bootstrap_application()

    module = FakeModule()

    manifests = (
        ModuleManifest(
            name="fake",
            module=module,
        ),
    )

    context = ModuleSetupContext()

    load_modules(
        manifests=manifests,
        context=context,
    )

    assert module.loaded is True
