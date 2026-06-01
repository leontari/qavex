from __future__ import annotations

import pytest

from template_app.launcher.exceptions import CompositionViolationError
from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_direct_bootstrap_forbidden() -> None:
    with pytest.raises(CompositionViolationError):
        bootstrap_kernel()


def test_builder_can_create_kernel() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    assert composition.kernel is not None
