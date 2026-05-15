"""Tests for local development entrypoint."""

from __future__ import annotations

from unittest.mock import patch

from template_app.main import main


def test_main_runs_uvicorn() -> None:
    """Ensure uvicorn.run is called."""

    with patch("template_app.main.uvicorn.run") as mock_run:
        main()

    _, kwargs = mock_run.call_args

    assert kwargs["host"] == "127.0.0.1"
    assert kwargs["port"] == 8000
    assert kwargs["log_config"] is None
    assert isinstance(kwargs["reload"], bool)
