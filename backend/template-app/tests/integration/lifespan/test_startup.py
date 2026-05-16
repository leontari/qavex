from __future__ import annotations

from fastapi.testclient import TestClient

from template_app.asgi import app



def test_application_startup_hooks_execute() -> None:
    with (TestClient(app)):
        context = app.state.context

        hooks = context.runtime.lifecycle_registry.startup_hooks

        assert len(hooks) > 0
