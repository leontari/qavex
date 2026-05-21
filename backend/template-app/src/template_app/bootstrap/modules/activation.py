"""Module runtime activation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.context import ModuleSetupContext
    from template_app.bootstrap.modules.manifests import ModuleManifest


def activate_module(
    manifest: ModuleManifest,
    context: ModuleSetupContext,
) -> None:
    """
    Activate a single module.

    One manifest -> one scoped context.

    This is the ONLY allowed entrypoint for a module's execution.
    """
    manifest.module.setup(context)
