from __future__ import annotations

import pytest

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from tests.support.fakes.transports import FakeTransport


def test_launcher_build_freezes_kernel() -> None:
    launcher = KernelLauncher(
        LauncherConfig(mode=LaunchMode.HTTP),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True


def test_transport_install_after_freeze_fails() -> None:
    launcher = KernelLauncher(
        LauncherConfig(mode=LaunchMode.HTTP),
    )

    composition = launcher.build()

    with pytest.raises(RuntimeError):
        composition.kernel.install_transport(FakeTransport())
