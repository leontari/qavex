"""
Interception point.

can be used for:
- logging
- tracing
- sandboxing
- permissions
- dependency injection validation

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.module.manifests import ModuleManifest


def activate_module(
    manifest: ModuleManifest,
) -> ModuleManifest:
    """
    Activate module manifest.

    It does nothing for now but later can be extended for:
    - feature flags
    - license checks
    - dependency validation
    - version compatibility
    - environment filters

    Returns:
        ModuleManifest

    """
    return manifest
