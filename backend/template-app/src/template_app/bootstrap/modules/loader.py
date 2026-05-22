"""The entrypoint for module loading into kernel context."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules.activation import activate_module
from template_app.bootstrap.modules.context import ModuleSetupContext

if TYPE_CHECKING:
    from template_app.bootstrap.modules.apis import (
        ModuleInfraAPI,
        ModuleMessagingAPI,
        ModuleRuntimeAPI,
    )
    from template_app.bootstrap.modules.manifests import ModuleManifest


def load_modules(
    manifests: tuple[ModuleManifest, ...],
    runtime_api: ModuleRuntimeAPI,
    infra_api: ModuleInfraAPI,
    messaging_api: ModuleMessagingAPI,
) -> None:
    """
    Load and execute the module activation.

    This is used by bootstrap only.
    """
    for manifest in manifests:
        context = ModuleSetupContext(
            runtime=runtime_api,
            infra=infra_api,
            messaging=messaging_api,
            capabilities=manifest.capabilities,
        )

        activate_module(
            manifest=manifest,
            context=context,
        )
