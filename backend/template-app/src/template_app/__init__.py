"""
Package root.

This module:
  * exposes the application instance for external runners
  * enables running the application by the next command:
        uvicorn template_app:app

Note:
    Due to this module the import performed by uvicorn:
        template_app:app
    is equivalent to:
        from template_app.main import app

"""

from __future__ import annotations

from template_app.main import app

__all__ = ["app"]
