from __future__ import annotations


def test_asgi_app_importable() -> None:
    """ASGI app must be import-safe."""
    from fastapi import FastAPI
    from template_app.asgi import app

    assert isinstance(app, FastAPI)


def test_asgi_kernel_initialized() -> None:
    """Runtime kernel must be initialized at import time."""
    from template_app.asgi import kernel
    from template_app.runtime.kernel.kernel import RuntimeKernel
    assert kernel is not None
    assert isinstance(kernel, RuntimeKernel)
