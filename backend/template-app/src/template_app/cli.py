"""CLI entrypoint."""

from __future__ import annotations


def main():
    kernel = bootstrap()
    launcher = KernelLauncher(kernel)

    mode = sys.argv[1]
    launcher.run(mode)


if __name__ == "__main__":
    main()
