"""gRPC runtime entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.kernel.bootstrap import bootstrap_kernel

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def main() -> None:
    """Run gRPC runtime."""
    config = LauncherConfig(mode=LaunchMode.GRPC)

    kernel: RuntimeKernel = bootstrap_kernel()

    launcher = KernelLauncher(
        _kernel=kernel,
        _config=config,
    )

    launcher.run()


if __name__ == "__main__":
    main()
