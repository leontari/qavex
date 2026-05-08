"""
Development entry point.

This module is intended ONLY for local development.
It allows running the application directly from an IDE or via Python.
Example command from the project root source folder:
    python backend/template-app/src/template_app/main.py

Production environments must use an external ASGI runner, for example:
    uvicorn template_app:app --host 0.0.0.0 --port 8000 --log-config path/to/logging.json

Note:
    'template_app:app' is interpreted by uvicorn as:
        from template_app import app
    which is equivalent to:
        from template_app.main import app
"""
import logging
from fastapi import FastAPI
from template_app.core.app.logging import setup_logging


def create_app() -> FastAPI:

    logger = logging.getLogger(__name__)

    app = FastAPI()
    logger.info(f"Application starting...")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_config="../template_app/config/logging.yaml",
    )
