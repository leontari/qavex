"""
Local development entry point.

This module exists solely to support running the application directly
via Python or an IDE during development. It initializes logging,
constructs the FastAPI application, and starts an Uvicorn server when
executed as a script.

Production environments must not use this module. Instead, an external
ASGI server should import the application from `template_app`, for example:

    uvicorn template_app:app --host 0.0.0.0 --port 8000

This separation ensures that production deployments avoid development-only
side effects and rely on a clean, import-based ASGI entry point.

"""

from __future__ import annotations

if __name__ == "__main__":
    import pathlib

    import uvicorn

    # Resolve logging config relative to this file
    BASE_DIR = pathlib.Path(__file__).resolve().parent  # /template-app
    CONFIG_PATH = BASE_DIR / "config" / "logger.yaml"

    uvicorn.run(
        "template_app:app",
        host="127.0.0.1",
        port=8000,
        log_config=str(CONFIG_PATH),
        reload=True,
        reload_dirs=str(BASE_DIR),
    )
