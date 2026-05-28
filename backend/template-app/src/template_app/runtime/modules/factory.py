"""Module boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.module.context import ModuleContext

if TYPE_CHECKING:
    from template_app.runtime.kernel import RuntimeKernel
    from template_app.runtime.module.manifests import ModuleManifest


def build_module_context(
    kernel: RuntimeKernel,
    manifest: ModuleManifest,
) -> ModuleContext:

    return ModuleContext(
        runtime=kernel.build_runtime_api(),
        infra=kernel.build_infra_api(),
        messaging=kernel.build_messaging_api(),
        capabilities=manifest.capabilities,
    )
