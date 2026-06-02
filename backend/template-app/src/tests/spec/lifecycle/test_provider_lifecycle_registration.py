from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder


def test_runtime_contains_lifecycle() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert composition.kernel.lifecycle is not None
