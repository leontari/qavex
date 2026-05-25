"""CLI entrypoint."""

from __future__ import annotations

import sys

from template_app.launcher.run import KernelLauncher
from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def main():
    kernel = bootstrap_kernel()

    launcher = KernelLauncher(kernel)

    mode = sys.argv[1]
    launcher.run(mode)


if __name__ == "__main__":
    main()
