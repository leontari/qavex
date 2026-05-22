"""The entrypoint for the kernel runtime bootstrap."""

from __future__ import annotations

from template_app.bootstrap.modules.capabilities import ModuleCapability
from template_app.bootstrap.modules.context import ModuleSetupContext
from template_app.bootstrap.modules.loader import load_modules
from template_app.bootstrap.modules.manifests import ModuleManifest
from template_app.bootstrap.modules.registry import ModuleRegistry
from template_app.bootstrap.modules.setup import setup_modules

__all__ = [
    "ModuleCapability",
    "ModuleManifest",
    "ModuleRegistry",
    "ModuleSetupContext",
    "load_modules",
    "setup_modules",
]
