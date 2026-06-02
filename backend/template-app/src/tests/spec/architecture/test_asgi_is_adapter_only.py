from __future__ import annotations

from pathlib import Path


ASGI_FILE = Path("template_app/asgi.py")


def test_asgi_does_not_use_builder() -> None:
    source = ASGI_FILE.read_text()

    assert "ApplicationBuilder" not in source


def test_asgi_does_not_use_bootstrap_kernel() -> None:
    source = ASGI_FILE.read_text()

    assert "bootstrap_kernel" not in source


def test_asgi_does_not_create_fastapi() -> None:
    source = ASGI_FILE.read_text()

    assert "FastAPI(" not in source
