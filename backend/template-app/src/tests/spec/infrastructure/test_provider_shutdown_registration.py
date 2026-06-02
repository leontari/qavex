from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder


def test_shutdown_registry_exists() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert composition.kernel.lifecycle.registry is not None
