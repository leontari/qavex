"""Module boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules.context import ModuleSetupContext

if TYPE_CHECKING:
    from template_app.bootstrap.kernel import RuntimeKernel
    from template_app.bootstrap.modules.manifests import ModuleManifest


def build_module_context(
    kernel: RuntimeKernel,
    manifest: ModuleManifest,
) -> ModuleSetupContext:

    return ModuleSetupContext(
        runtime=kernel.build_runtime_api(),
        infra=kernel.build_infra_api(),
        messaging=kernel.build_mesaging_api(),
        capabilities=manifest.capabilities,
    )
