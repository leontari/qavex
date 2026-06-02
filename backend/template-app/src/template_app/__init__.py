"""
Template App package.

Import-safe package root.

Important:
    Application composition MUST NOT happen here.

Package import MUST NOT trigger:
    - kernel bootstrap
    - transport creation
    - application composition
    - plugin discovery
    - DI initialization

Runtime entrypoints:
    template_app.asgi:app
    template_app.main:main

"""

from __future__ import annotations

__version__ = "0.3.0"

__all__ = ("__version__",)
