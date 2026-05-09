"""
The application's entry point.

This module:
  * can be used directly ONLY within local development
  * allows to run the application from an IDE or Python

Command to run the application from the workspace root folder:
    python backend/template-app/src/template_app/main.py

Note:
Production environments must use an external ASGI runner, for example:
    uvicorn template_app:app --host 0.0.0.0 --port 8000

"""

from __future__ import annotations

from template_app.core.app.factory import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_config="../template_app/config/logging.yaml",
    )
