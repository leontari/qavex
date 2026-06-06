from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.container import Container


def test_runtime_contains_container() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    assert isinstance(composition.kernel.runtime.container, Container)
