"""HTTP runtime entrypoint."""

from __future__ import annotations

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def main() -> None:
    """Run HTTP runtime."""
    kernel = bootstrap_kernel()

    launcher = KernelLauncher(
        _kernel=kernel,
        _config=LauncherConfig(mode=LaunchMode.HTTP),
    )

    launcher.run()


if __name__ == "__main__":
    main()
