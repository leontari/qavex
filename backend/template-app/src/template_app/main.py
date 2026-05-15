"""Local development entrypoint."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main() -> None:
    """Run local development server."""
    is_test = os.getenv("PYTEST_CURRENT_TEST") is not None

    uvicorn.run(
        "template_app:app",
        host="127.0.0.1",
        port=8000,
        reload=not is_test,
        log_config=None,
    )


if __name__ == "__main__":
    main()
