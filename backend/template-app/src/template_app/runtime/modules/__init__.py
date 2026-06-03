"""The entrypoint for the kernel runtime bootstrap."""

from __future__ import annotations

from template_app.runtime.modules.capabilities import ModuleCapability
from template_app.runtime.modules.context import ModuleContext
from template_app.runtime.modules.loader import load_modules
from template_app.runtime.modules.manifests import ModuleManifest
from template_app.runtime.modules.registry import ModuleRegistry
from template_app.runtime.modules.setup import setup_modules

__all__ = [
    "ModuleCapability",
    "ModuleContext",
    "ModuleManifest",
    "ModuleRegistry",
    "load_modules",
    "setup_modules",
]
