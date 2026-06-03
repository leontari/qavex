"""Module lifecycle orchestration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.modules.activation import activate_module
from template_app.runtime.modules.discovery import discover_modules
from template_app.runtime.modules.loader import load_modules

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from template_app.runtime.modules.context import ModuleContext
    from template_app.runtime.modules.manifests import ModuleManifest
    from template_app.runtime.modules.registry import ModuleRegistry


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
    """Activate discovered modules."""

    return tuple(activate_module(manifest) for manifest in manifests)


def load(
    manifests: Iterable[ModuleManifest],
    context_factory: Callable[[ModuleManifest], ModuleContext],
) -> None:
    """Load activated modules."""

    for manifest in manifests:
        context = context_factory(manifest)

        load_modules(
            manifest=manifest,
            context=context,
        )
