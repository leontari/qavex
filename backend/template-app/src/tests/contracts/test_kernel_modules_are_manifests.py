from template_app.bootstrap.modules.manifests import (
    ModuleManifest,
)
from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_kernel_modules_are_manifests() -> None:
    kernel = bootstrap_application()

    assert all(
        isinstance(module, ModuleManifest)
        for module in kernel.modules
    )
