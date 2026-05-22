from __future__ import annotations

from template_app.bootstrap.modules import (
    ModuleCapability,
    ModuleManifest,
)
from template_app.bootstrap.modules.lifecycle import (
    load,
)

from tests.factories.module_context import (
    build_module_context,
)


class FakeModule:

    loaded: bool = False

    def setup(self, context) -> None:
        self.loaded = True


def test_loader_executes_module_setup() -> None:
    module = FakeModule()

    manifests = (
        ModuleManifest(
            name="fake",
            module=module,
            capabilities=frozenset({
                ModuleCapability.ROUTER,
            }),
        ),
    )

    def context_factory(
        manifest: ModuleManifest,
    ):
        return build_module_context(
            capabilities=manifest.capabilities,
        )

    load(
        manifests=manifests,
        context_factory=context_factory,
    )

    assert module.loaded is True
