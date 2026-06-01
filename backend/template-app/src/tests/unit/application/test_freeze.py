from __future__ import annotations

import pytest

from template_app.runtime.application.builder import (
    ApplicationBuilder,
)


def test_kernel_is_frozen_after_builder_freeze() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    builder.freeze(composition)

    assert composition.kernel.is_frozen is True


def test_transport_install_after_freeze_fails() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    builder.freeze(composition)

    with pytest.raises(RuntimeError):
        composition.kernel.install_transport(object())
