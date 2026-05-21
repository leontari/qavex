"""Module runtime activation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.context import ModuleSetupContext
    from template_app.bootstrap.modules.manifest import ModuleManifest


def load_modules(
    manifest: ModuleManifest,
    context: ModuleSetupContext,
) -> None:
    """
    Activate application module.

    One manifest -> one scoped context.
    """
    manifest.module.setup(context)
