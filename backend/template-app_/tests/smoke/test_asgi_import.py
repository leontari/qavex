from __future__ import annotations

from unittest.mock import patch

from fastapi import FastAPI


# module import, app exists, app created, logging bootstrap invoked
@patch("template_app.asgi.setup_logging")
def test_asgi_app_importable(mock_logging) -> None:
    from template_app.asgi import app

    assert isinstance(app, FastAPI)

    mock_logging.assert_called_once()


@patch("template_app.asgi.bootstrap_application")
def test_asgi_import(mock_bootstrap):
    from template_app.asgi import app

    assert app is not None

    mock_bootstrap.assert_called_once()
