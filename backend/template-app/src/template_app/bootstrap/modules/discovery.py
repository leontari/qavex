"""enable/disable/filtering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.manifest import ModuleManifest
    from template_app.bootstrap.modules.registry import ModuleRegistry


def discover_modules(registry: ModuleRegistry) -> tuple[ModuleManifest, ...]:
    """Discover enabled modules."""
    return tuple(manifest for manifest in registry.modules if manifest.enabled)
