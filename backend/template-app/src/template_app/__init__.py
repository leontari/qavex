"""
Expose the FastAPI application instance for external runners.

This allows running the service using commands like:
    uvicorn template_app:app

The actual application object is created in `main.py` and re-exported here
to provide a clean public entry point for ASGI servers.
"""
from __future__ import annotations

from template_app.main import app

__all__ = ["app"]
