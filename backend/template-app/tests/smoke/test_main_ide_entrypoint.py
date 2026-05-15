"""Smoke test for IDE startup."""

from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest


def get_free_port() -> int:
    """Return free TCP port."""

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.mark.smoke
def test_main_py_starts_application() -> None:
    """
    Ensure direct execution of main.py starts app correctly.
    """

    port = get_free_port()

    project_root = Path(__file__).resolve().parents[2]

    main_py = (
        project_root
        / "src"
        / "template_app"
        / "main.py"
    )

    env = os.environ.copy()
    env["PORT"] = str(port)
    env["UVICORN_RELOAD"] = "false"

    process = subprocess.Popen(
        [sys.executable, str(main_py)],
        cwd=project_root,
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )

    try:
        deadline = time.time() + 15

        while time.time() < deadline:
            if process.poll() is not None:
                pytest.fail(
                    f"Application exited with code {process.returncode}",
                )

            try:
                response = httpx.get(
                    f"http://127.0.0.1:{port}/health",
                    timeout=1,
                )

                assert response.status_code == 200
                return

            except Exception:
                time.sleep(0.5)

        pytest.fail("Application never became ready")

    finally:
        if process.poll() is None:
            process.send_signal(signal.CTRL_BREAK_EVENT)

            time.sleep(2)

            if process.poll() is None:
                process.kill()
