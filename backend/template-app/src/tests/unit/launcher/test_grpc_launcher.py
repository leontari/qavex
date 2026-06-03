from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.grpc.transport import GRPCTransport


def test_grpc_launcher_installs_grpc_transport() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.GRPC,
        ),
    )

    composition = launcher.build()
    transport = composition.kernel.transport_manager.get(GRPCTransport)

    assert transport is not None


def test_grpc_launcher_freezes_kernel() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.GRPC,
        ),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True
