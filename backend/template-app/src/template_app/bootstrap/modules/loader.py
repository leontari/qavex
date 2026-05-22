"""Module loader."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.context import ModuleSetupContext
    from template_app.bootstrap.modules.manifests import ModuleManifest


def load_modules(
    manifest: ModuleManifest,
    context: ModuleSetupContext,
) -> None:
    """Execute module setup."""
    manifest.module.setup(context)
