from __future__ import annotations

from fastapi import FastAPI

from template_app.asgi import app


def test_asgi_exports_fastapi_app() -> None:
    assert isinstance(app, FastAPI)


def test_asgi_app_has_routes() -> None:
    assert len(app.routes) > 0


def test_asgi_app_title_exists() -> None:
    assert app.title is not None
