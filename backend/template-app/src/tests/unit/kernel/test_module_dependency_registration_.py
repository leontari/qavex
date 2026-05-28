from __future__ import annotations

from template_app.runtime.modules.manifests import (
    ModuleManifest,
)

from tests.support.factories.kernel import (
    build_testing_kernel,
)


def test_module_can_register_dependency() -> None:

    kernel = build_testing_kernel()

    manifest = ModuleManifest(
        name="test",
        version="1.0.0",
        dependencies=frozenset({
            "database",
        }),
    )

    kernel.context.runtime.modules.registry.register(
        manifest,
    )

    installed = (
        kernel.context
        .runtime
        .modules
        .registry
        .modules
    )

    assert manifest in installed
