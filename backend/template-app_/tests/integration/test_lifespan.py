from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from template_app import app


@patch("template_app.core.lifecycle.startup.connect_db", new_callable=AsyncMock)
@patch("template_app.core.lifecycle.startup.connect_redis", new_callable=AsyncMock)
def test_startup(
    mock_redis,
    mock_db,
):
    with TestClient(app):
        pass

    mock_db.assert_awaited_once()
    mock_redis.assert_awaited_once()
