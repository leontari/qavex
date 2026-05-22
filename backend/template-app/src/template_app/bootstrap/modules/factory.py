"""Module boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.bootstrap.modules.context import ModuleSetupContext

if TYPE_CHECKING:
    from template_app.bootstrap.kernel import RuntimeKernel
    from template_app.bootstrap.modules.manifests import ModuleManifest


def build_module_context(
    kernel: RuntimeKernel, manifest: ModuleManifest
) -> ModuleSetupContext:
    runtime_api = ModuleRuntimeAPI(
        app=kernel.context.app,
        container=kernel.context.runtime.container,
        lifecycle_registry=kernel.context.runtime.lifecycle_registry,
    )

    infra_api = ModuleInfraAPI(
        registry=kernel.context.runtime.infrastructure_registry,
    )

    messaging_api = ModuleMessagingAPI(
        event_bus=kernel.context.runtime.event_bus,
        command_bus=kernel.context.runtime.command_bus,
        query_bus=kernel.context.runtime.query_bus,
    )

    return ModuleSetupContext(
        runtime=runtime_api,
        infra=infra_api,
        messaging=messaging_api,
        capabilities=manifest.capabilities,
    )
