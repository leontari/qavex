from __future__ import annotations

from fastapi import FastAPI


def test_asgi_exports_fastapi_app() -> None:
    from template_app.asgi import app

    assert isinstance(app, FastAPI)
