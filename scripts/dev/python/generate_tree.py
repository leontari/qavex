#!/usr/bin/env python3
"""
Generate project structure.

Utility module for generating a human-readable directory tree structure.

This module provides a simple way to inspect and document the structure of a
project repository. It recursively scans a given root directory and produces a
text-based tree representation similar to the output of Unix `tree`, but with
clean formatting suitable for documentation or code reviews.

Typical usage example:
----------------------

    python generate_tree.py /path/to/project

The output will look like:

    project/
    ├── src
    │   ├── module
    │   │   └── file.py
    └── README.md

Functions
---------
build_tree(root: Path, prefix: str = "") -> str
    Recursively constructs a directory tree representation.

generate_project_structure(root_path: str) -> str
    Generates a complete directory tree for the given project root.

This module can be imported and used programmatically or
executed as a CLI tool.
"""

from __future__ import annotations

from pathlib import Path

IGNORE_DIRS = {"__pycache__", ".git", ".venv", ".idea", ".mypy_cache"}
IGNORE_EXT = {".pyc", ".pyo", ".pyd", ".DS_Store"}


def should_ignore(entry: Path) -> bool:
    """
    Determine whether a filesystem entry should be excluded from the tree.

    Parameters
    ----------
    entry : Path
        A filesystem object (file or directory) that should be evaluated
        against the ignore rules.

    Returns
    -------
    bool
        True if the entry must be ignored and excluded from the output.
        False if the entry should be included.

    """
    if entry.name in IGNORE_DIRS:
        return True
    return entry.suffix in IGNORE_EXT


def build_tree(root: Path, prefix: str = "") -> str:
    """
    Recursively build a formatted directory tree.

    Parameters
    ----------
    root : Path
        Directory to scan.
    prefix : str, optional
        Prefix used internally for indentation of nested levels.

    Returns
    -------
    str
        Multiline string representing the directory structure.

    Notes
    -----
    - Directories are listed before files.
    - Entries are sorted alphabetically.
    - The output uses Unicode box-drawing characters.

    """
    entries = sorted(
        (e for e in root.iterdir() if not should_ignore(e)),
        key=lambda p: (p.is_file(), p.name.lower()),
    )

    lines = []

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        line = f"{prefix}{connector}{entry.name}"
        lines.append(line)

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.append(build_tree(entry, prefix + extension))

    return "\n".join(lines)


def generate_project_structure(root_path: str) -> str:
    """
    Generate a directory tree for the given project root.

    Parameters
    ----------
    root_path : str
        Path to the root directory of the project.

    Returns
    -------
    str
        A formatted directory tree beginning with the root folder name.

    Raises
    ------
    ValueError
        If the provided path does not exist.

    Examples
    --------
    >>> print(generate_project_structure("./src"))
    src/
    ├── module
    │   └── file.py
    └── README.md

    """
    root = Path(root_path).resolve()
    if not root.exists():
        msg = f"Path does not exist: {root}"
        raise ValueError(msg)

    header = f"{root.name}/"
    body = build_tree(root)
    return f"{header}\n{body}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate directory tree for a project."
    )
    parser.add_argument("path", help="Path to project root")

    args = parser.parse_args()
    print(generate_project_structure(args.path))  # noqa: T201
