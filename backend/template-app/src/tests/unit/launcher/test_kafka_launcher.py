from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.kafka.transport import KafkaTransport


def test_kafka_launcher_installs_kafka_transport() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.KAFKA,
        ),
    )

    composition = launcher.build()
    transport = composition.kernel.transport_manager.get(KafkaTransport)

    assert transport is not None


def test_kafka_launcher_freezes_kernel() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.KAFKA,
        ),
    )

    composition = launcher.build()

    assert composition.kernel.is_frozen is True
