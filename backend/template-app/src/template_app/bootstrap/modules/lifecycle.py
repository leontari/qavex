"""
Module lifecycle orchestration.

The flow of the modules plugging into kernel:
    discover_modules()
        ↓
    load_modules()
        ↓
    activate_module()
        ↓
    Module.setup(context)


In other words::
    Manifest
        ↓
    setup modules' isolated context
        ↓
    activation

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.modules import discover_modules, load_modules
from template_app.bootstrap.modules.activation import activate_module
from template_app.bootstrap.modules.context import ModuleSetupContext

if TYPE_CHECKING:
    from typing import Iterable

    from template_app.bootstrap.modules.apis import (
        ModuleInfraAPI,
        ModuleMessagingAPI,
        ModuleRuntimeAPI,
    )
    from template_app.bootstrap.modules.manifests import ModuleManifest
    from template_app.bootstrap.modules.registry import ModuleRegistry


def discover(registry: ModuleRegistry) -> tuple[ModuleManifest, ...]:
    """
    Discover registered modules.

    Get list of manifests registered in module registry

    Returns:
        an immutable list of enabled modules

    """
    return discover_modules(registry)


def activate(
    manifests: Iterable[ModuleManifest],
) -> tuple[ModuleManifest, ...]:
    """Activate enabled modules."""

    return tuple(activate_module(manifests) for manifest in manifests)


def load(
    manifests: Iterable[ModuleManifest],
    contest_factory,
) -> None:
    """Load activated modules."""

    for manifest in manifests:
        context = contest_factory(manifest)

        load_module(
            manifest=manifest,
            context=context,
        )


# def activate_module(
#     manifest: ModuleManifest,
#     context: ModuleSetupContext,
# ) -> None:
#     """
#     Activate a single module.
#
#     One manifest -> one scoped context.
#
#     This is the ONLY allowed entrypoint for a module's execution.
#     """
#     manifest.module.setup(context)


# def load_modules(
#     manifests: tuple[ModuleManifest, ...],
#     runtime_api: ModuleRuntimeAPI,
#     infra_api: ModuleInfraAPI,
#     messaging_api: ModuleMessagingAPI,
# ) -> None:
#     """
#     Load and execute the module activation in the kernel.
#
#     This is used by bootstrap only.
#     """
#     for manifest in manifests:
#
#         context = ModuleSetupContext(
#             runtime=runtime_api,
#             infra=infra_api,
#             messaging=messaging_api,
#             capabilities=manifest.capabilities,
#         )
#
#         activate_module(
#             manifest=manifest,
#             context=context,
#         )
