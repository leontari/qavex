"""
Application package entry point.

This module exposes the ASGI application instance so that external ASGI
servers (such as Uvicorn or Gunicorn) can import and run the service
without executing any development-only code.

It enables commands like:

    uvicorn template_app:app

The actual application construction and configuration are defined in
`template_app.asgi`, which provides a clean separation between the
runtime entry point and the application factory.
"""

from __future__ import annotations

from template_app.asgi import app

__all__ = ["app"]
