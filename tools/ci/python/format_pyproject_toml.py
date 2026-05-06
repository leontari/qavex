#!/usr/bin/env python3
"""
Wrapper for pyproject-fmt used in CI with prek.

Reason:
    - pyproject-fmt requires explicit file paths as positional arguments.
    - prek cannot pass files to pyproject-fmt directly during CI checks and
      requires explicit file listing in the config.
    - pyproject-fmt fails when invoked without file paths and has no file
      discovery support.
    - This wrapper receives filenames from prek and forwards them to
      pyproject_fmt.run().
"""

from __future__ import annotations

import sys
from pathlib import Path

import pyproject_fmt  # type: ignore  # noqa: PGH003


def main() -> int:
    """
    Format all provided pyproject.toml files.

    Returns:
        int: 0 on success, non-zero if any file fails to format.

    """
    files: list[str] = sys.argv[1:]
    if not files:
        return 0

    for file_path in files:
        path = Path(file_path)

        if not path.is_file():
            sys.stdout.write(f"Skipping non-file: {path}")
            continue

        sys.stdout.write(f"Formatting: {path}")
        try:
            # run() expects a list of CLI arguments (strings)
            pyproject_fmt.run([str(path)])
        except Exception as exc:  # noqa: BLE001
            sys.stdout.write(f"Error formatting {path}: {exc}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
