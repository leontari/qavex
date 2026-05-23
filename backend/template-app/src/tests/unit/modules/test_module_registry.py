from template_app.runtime.module.manifests import ModuleManifest
from template_app.runtime.module.registry import ModuleRegistry


class FakeModule:
    def setup(self, context) -> None:
        pass


def test_module_registry_registers_manifest() -> None:
    registry = ModuleRegistry()

    manifest = ModuleManifest(
        name="fake",
        module=FakeModule(),
    )

    registry.register(manifest)

    assert registry.get("fake") is manifest


def test_module_registry_returns_tuple() -> None:
    registry = ModuleRegistry()

    registry.register(
        ModuleManifest(
            name="fake",
            module=FakeModule(),
        )
    )

    assert isinstance(registry.modules, tuple)
