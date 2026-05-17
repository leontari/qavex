"""
Template App package entry point.

This module exposes the ASGI application instance for production-grade
import-based execution.

Supported runtimes include:

- Uvicorn
- Gunicorn + Uvicorn workers
- Kubernetes deployments
- Docker containers
- wheel installations

Example:
    uvicorn template_app:app

The actual application construction is delegated to `template_app.asgi`
to keep the package entry point lightweight and side effect free.

"""

from __future__ import annotations

from template_app.asgi import app

__all__ = ["app"]
