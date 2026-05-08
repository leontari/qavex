"""
Expose the FastAPI application instance for external runners.

This enables running the service using commands like:
    uvicorn template_app:app

Explanation:
    The package 'template_app' re‑exports the FastAPI instance from
    template_app.main, so the import performed by uvicorn:

        template_app:app

    is equivalent to:
        from template_app.main import app
"""
from template_app.main import app
from template_app.core.logging import setup_logging

setup_logging()

__version__ = "0.1.0"
__all__ = ["app"]
