from __future__ import annotations

from fastapi import FastAPI

from template_app.core_.app_.factory import create_app


def test_create_app_returns_fastapi() -> None:
    app = create_app()

    assert isinstance(app, FastAPI)
