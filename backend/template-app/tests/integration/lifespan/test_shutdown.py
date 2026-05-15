from __future__ import annotations

from fastapi.testclient import TestClient

from template_app.asgi import app



def test_application_shutdown_hooks_registered() -> None:
    with TestClient(app):
        hooks = app.state.lifecycle_registry.shutdown_hooks

        assert len(hooks) > 0
