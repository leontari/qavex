"""Module loader."""

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
    manifest: ModuleManifest,
    context: ModuleSetupContext,
) -> None:
    """Execute module setup."""
    manifest.module.setup(context)
