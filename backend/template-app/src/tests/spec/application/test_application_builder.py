from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.application.composition import ApplicationComposition


def test_builder_creates_composition() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert isinstance(composition, ApplicationComposition)


def test_builder_creates_kernel() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert composition.kernel is not None


def test_builder_starts_with_empty_transport_collection() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert composition.transports == []
