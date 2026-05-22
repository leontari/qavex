"""
Module system bootstrap.

The flow of the modules plugging into kernel:
    discover_modules()
        ↓
    load_modules()
        ↓
    activate_module()
        ↓
    Module.setup(context)


Modules pipeline:
    Manifest
        ↓
    setup isolated context
        ↓
    activation


Setup injects/installs modules' contexts into the kernel's runtime state.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.bootstrap.modules.context import (
    ModuleSetupContext,
)
from template_app.bootstrap.modules.lifecycle import (
    activate,
    discover,
    load,
)

if TYPE_CHECKING:
    from template_app.bootstrap.kernel import RuntimeKernel
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
    Set up pluggable runtime modules.

    Responsibilities:
    - discover modules
    - activate modules
    - create module contexts
    - inject modules into runtime

    Returns:
        tuple[ModuleManifest, ...]:
            installed module manifests

    """
    manifests = discover(registry)
    manifests = activate(manifests)
    runtime = kernel.context.runtime

    runtime_api = ModuleRuntimeAPI(
        app=kernel.app,
        container=runtime.container,
        lifecycle_registry=runtime.lifecycle_registry,
    )

    infra_api = ModuleInfraAPI(
        registry=runtime.infrastructure_registry,
    )

    messaging_api = ModuleMessagingAPI(
        event_bus=runtime.event_bus,
        command_bus=runtime.command_bus,
        query_bus=runtime.query_bus,
    )

    def context_factory(
        manifest: ModuleManifest,
    ) -> ModuleSetupContext:

        return ModuleSetupContext(
            runtime=runtime_api,
            infra=infra_api,
            messaging=messaging_api,
            capabilities=manifest.capabilities,
        )

    load(
        manifests=manifests,
        context_factory=context_factory,
    )

    return manifests
