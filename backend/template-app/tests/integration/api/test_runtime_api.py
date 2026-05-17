from __future__ import annotations

from fastapi.testclient import TestClient

from template_app.asgi import app


client = TestClient(app)


def test_runtime_endpoint() -> None:
    response = client.get("/runtime")

    assert response.status_code == 200

    assert response.json() == {
        "runtime": "active",
    }
