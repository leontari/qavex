"""
Template App package entrypoint.

Production runtimes should import:

    template_app:app

Supported runtimes:

- uvicorn
- gunicorn
- kubernetes
- docker
- pytest

The package entrypoint must remain lightweight and import-safe.
"""

from __future__ import annotations

from template_app.asgi import app

__version__ = "0.3.0"

__all__ = ["app"]
