"""Module loader."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.modules.context import ModuleContext
    from template_app.runtime.modules.manifests import ModuleManifest


def load_modules(
    manifest: ModuleManifest,
    context: ModuleContext,
) -> None:
    """Execute module setup."""
    manifest.module.setup(context)
