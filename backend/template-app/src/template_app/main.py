"""Local development entrypoint."""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Run local development server."""
    uvicorn.run(
        "template_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=None,
    )


if __name__ == "__main__":
    main()
