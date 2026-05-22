"""enable/disable/filter modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.manifests import ModuleManifest
    from template_app.bootstrap.modules.registry import ModuleRegistry


def discover_modules(registry: ModuleRegistry) -> tuple[ModuleManifest, ...]:
    """
    Discover enabled modules.

    registry → manifests

    Returns:
        an immutable list of enabled modules

    """
    return tuple(
        manifest for manifest in registry.modules if manifest.enabled
    )  # TODO: recheck
