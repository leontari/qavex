"""
Module system bootstrap.

Setups injects/installs modules' contexts into the kernel's runtime state.

The flow:
---------
bootstrap/runtime/bootstrap.py
    ↓
setup_modules()

modules/setup.py
    ↓
discover()
activate()
load()
    ↓
modules/factory.py
    ↓
build_module_context()

modules/lifecycle.py
    ↓
load_module()

modules/loader.py
    ↓
module.setup(context)

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules.factory import (
    build_module_context,
)
from template_app.bootstrap.modules.lifecycle import (
    activate,
    discover,
    load,
)

if TYPE_CHECKING:
    from template_app.bootstrap.kernel import RuntimeKernel
    from template_app.bootstrap.modules.context import ModuleSetupContext
    from template_app.bootstrap.modules.manifests import (
        ModuleManifest,
    )
    from template_app.bootstrap.modules.registry import (
        ModuleRegistry,
    )


def setup_modules(
    kernel: RuntimeKernel,
    registry: ModuleRegistry,
) -> tuple[ModuleManifest, ...]:
    """
    Install pluggable runtime modules.

    Returns:
        tuple[ModuleManifest, ...]:
            installed module manifests

    """
    manifests = discover(registry)
    manifests = activate(manifests)

    def context_factory(
        manifest: ModuleManifest,
    ) -> ModuleSetupContext:

        return build_module_context(
            kernel=kernel,
            manifest=manifest,
        )

    load(
        manifests=manifests,
        context_factory=context_factory,
    )

    kernel.install_modules(manifests)

    return manifests
