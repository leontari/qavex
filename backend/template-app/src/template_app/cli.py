"""CLI entrypoint."""

from __future__ import annotations

import sys

from template_app.launcher.run import KernelLauncher
from template_app.runtime.bootstrap import bootstrap_kernel
from template_app.transports.cli.transport import CLITransport


def main():
    kernel = bootstrap_kernel()

    launcher = KernelLauncher(kernel)

    mode = sys.argv[1]
    launcher.run(mode)


if __name__ == "__main__":
    main()
