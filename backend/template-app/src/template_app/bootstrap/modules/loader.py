"""Module runtime activation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.context import ModuleSetupContext
    from template_app.bootstrap.modules.manifests import ModuleManifest


def load_modules(
    manifests: tuple[ModuleManifest, ...],
    context: ModuleSetupContext,
) -> None:
    """Load application modules."""

    for manifest in manifests:
        manifest.module.setup(context)
