"""The entrypoint for the kernel runtime bootstrap."""

from __future__ import annotations

from template_app.bootstrap.modules.setup import setup_modules

__all__ = [
    "setup_modules",
]
