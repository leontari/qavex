from __future__ import annotations

from fastapi.testclient import TestClient

from template_app.asgi import app



def test_application_shutdown_executes() -> None:
    with TestClient(app):
        pass
