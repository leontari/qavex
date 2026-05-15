"""
Local development entry point.

This module exists exclusively for local development and IDE execution.

Responsibilities:

- local Uvicorn execution
- development-only runtime bootstrap

Production environments MUST use import-based ASGI execution instead:

    uvicorn template_app:app

or:

    gunicorn template_app:app -k uvicorn.workers.UvicornWorker

This separation prevents accidental production usage of development-only
runtime logic.

"""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Run the local development server."""
    uvicorn.run(
        "template_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=None,
    )


if __name__ == "__main__":
    main()
