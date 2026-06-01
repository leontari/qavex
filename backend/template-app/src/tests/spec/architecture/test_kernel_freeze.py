from __future__ import annotations

from template_app.runtime.application.builder import (
    ApplicationBuilder,
)


def test_freeze_is_executed_once() -> None:

    builder = ApplicationBuilder()

    composition = builder.create()

    builder.freeze(composition)

    assert composition.kernel.is_frozen
