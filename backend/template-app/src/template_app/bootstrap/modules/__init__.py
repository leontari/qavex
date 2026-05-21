"""Business capability plugins."""

from __future__ import annotations

from template_app.bootstrap.modules.activation import load_modules
from template_app.bootstrap.modules.context import ModuleSetupContext
from template_app.bootstrap.modules.discovery import discover_modules
from template_app.bootstrap.modules.manifests import ModuleManifest
from template_app.bootstrap.modules.registry import ModuleRegistry

__all__ = [
    "ModuleManifest",
    "ModuleRegistry",
    "ModuleSetupContext",
    "discover_modules",
    "load_modules",
]
