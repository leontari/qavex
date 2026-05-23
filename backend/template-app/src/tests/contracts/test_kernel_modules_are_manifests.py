from template_app.runtime.module.manifests import (
    ModuleManifest,
)
from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_kernel_modules_are_manifests() -> None:
    kernel = bootstrap_kernel()

    assert all(
        isinstance(module, ModuleManifest)
        for module in kernel.modules
    )
