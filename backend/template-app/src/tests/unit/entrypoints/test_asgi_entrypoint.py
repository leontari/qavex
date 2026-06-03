from __future__ import annotations

from fastapi import FastAPI

from template_app import asgi


def test_asgi_exports_fastapi_app() -> None:
    assert isinstance(asgi.app, FastAPI)
