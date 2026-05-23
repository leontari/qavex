from template_app.runtime.module.discovery import discover_modules
from template_app.runtime.module.manifests import ModuleManifest
from template_app.runtime.module.registry import ModuleRegistry


class FakeModule:
    def setup(self, context) -> None:
        pass


def test_discovery_returns_enabled_modules() -> None:
    registry = ModuleRegistry()

    enabled = ModuleManifest(
        name="enabled",
        module=FakeModule(),
        enabled=True,
    )

    disabled = ModuleManifest(
        name="disabled",
        module=FakeModule(),
        enabled=False,
    )

    registry.register(enabled)
    registry.register(disabled)

    manifests = discover_modules(registry)

    assert enabled in manifests

    assert disabled not in manifests
