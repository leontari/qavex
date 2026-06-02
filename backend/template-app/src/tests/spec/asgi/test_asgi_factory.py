from __future__ import annotations

from fastapi import FastAPI

from template_app.launcher.facade import build_http_app


def test_http_factory_returns_fastapi() -> None:
    app = build_http_app()

    assert isinstance(app, FastAPI)


# def test_build_http_app_is_singleton() -> None:
#     first = build_http_app()
#     second = build_http_app()
#
#     assert first is second
