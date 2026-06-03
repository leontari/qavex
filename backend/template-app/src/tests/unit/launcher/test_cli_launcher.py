from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.cli.transport import CLITransport


def test_cli_launcher_installs_cli_transport() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.CLI,
        ),
    )

    composition = launcher.build()
    transport = composition.kernel.transport_manager.get(CLITransport)

    assert transport is not None


def test_cli_launcher_freezes_kernel() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.CLI,
        ),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True
