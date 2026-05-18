from template_app.bootstrap.modules.context import ModuleSetupContext
from template_app.bootstrap.modules.loader import load_modules
from template_app.bootstrap.modules.manifests import ModuleManifest
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


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

    context = ModuleSetupContext(_kernel=kernel)

    load_modules(
        manifests=manifests,
        context=context,
    )

    assert module.loaded is True
