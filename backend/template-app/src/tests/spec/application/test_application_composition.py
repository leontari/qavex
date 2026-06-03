from __future__ import annotations

import pytest

from template_app.launcher.config import LauncherConfig
from template_app.launcher.exceptions import CompositionViolationError
from template_app.launcher.run import KernelLauncher
from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.application.composition import ApplicationComposition
from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_launcher_build_returns_composition() -> None:
    composition = KernelLauncher(LauncherConfig()).build()

    assert isinstance(composition, ApplicationComposition)


def test_direct_kernel_bootstrap_forbidden() -> None:
    with pytest.raises(CompositionViolationError):
        bootstrap_kernel()


def test_builder_is_composition_layer() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    assert composition is not None


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
