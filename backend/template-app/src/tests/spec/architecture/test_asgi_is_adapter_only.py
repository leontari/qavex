from __future__ import annotations
import template_app.asgi
import inspect


def test_asgi_uses_facade() -> None:
    source = inspect.getsource(template_app.asgi)

    assert "build_http_app" in source


def test_asgi_does_not_use_builder() -> None:
    source = inspect.getsource(template_app.asgi)

    assert "ApplicationBuilder" not in source


def test_asgi_does_not_use_bootstrap_kernel() -> None:
    source = inspect.getsource(template_app.asgi)

    assert "bootstrap_kernel" not in source


def test_asgi_does_not_create_fastapi() -> None:
    source = inspect.getsource(template_app.asgi)

    assert "FastAPI(" not in source
