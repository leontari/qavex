#!/usr/bin/env python3
"""The generator for the dump of the project files."""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    ".idea",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
}


DEFAULT_PATTERNS = [
    "*.py",
    "*.toml",
    "*.yaml",
    "*.yml",
    "*.json",
    "*.md",
]


def should_exclude(path: Path) -> bool:
    """
    Check whether path should be excluded.

    Args:
        path:
            File or directory path.

    Returns:
        bool:
            True if path should be excluded.

    """
    return any(part in DEFAULT_EXCLUDES for part in path.parts)


def matches_patterns(
    path: Path,
    patterns: list[str],
) -> bool:
    """
    Check whether file matches allowed patterns.

    Args:
        path:
            File path.
        patterns:
            Allowed glob patterns.

    Returns:
        bool:
            True if file matches patterns.

    """
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def build_tree(root: Path) -> list[str]:
    """
    Build filesystem tree.

    Args:
        root:
            Root directory

    Returns:
        list[str]:
            Rendered directory tree lines.

    """
    lines: list[str] = []

    for path in sorted(root.rglob("*")):
        if should_exclude(path):
            continue

        depth = len(path.relative_to(root).parts)
        indent = "    " * (depth - 1)

        if path.is_dir():
            lines.append(f"{indent}[DIR] {path.name}")
        else:
            lines.append(f"{indent}[FILE] {path.name}")

    return lines


def collect_files(
    root: Path,
    patterns: list[str],
) -> list[Path]:
    """
    Collect source files.

    Args:
        root:
            Root directory.
        patterns:
            File match patterns.

    Returns:
        list[Path]:
            List of collected source files.

    """
    files: list[Path] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if should_exclude(path):
            continue
        if not matches_patterns(path, patterns):
            continue

        files.append(path)

    return files


def dump_project(
    root: Path,
    output_file: Path,
    patterns: list[str],
) -> None:
    """
    Dump project into single portable file.

    Writes project dump into output_file.

    Args:
        root:
            Project root directory.
        output_file:
            File patterns to include.
        patterns:
            File patterns to include.

    """
    tree = build_tree(root)

    files = collect_files(
        root=root,
        patterns=patterns,
    )

    with output_file.open("w", encoding="utf-8") as stream:
        stream.write("# PROJECT TREE\n\n")

        for line in tree:
            stream.write(f"{line}\n")

        stream.write("\n\n")

        for file_path in files:
            relative = file_path.relative_to(root)

            stream.write("=" * 80 + "\n")
            stream.write(f"FILE: {relative}\n")
            stream.write("=" * 80 + "\n\n")

            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                stream.write("[BINARY OR NON-UTF8 FILE]\n\n")
                continue

            stream.write(content)
            stream.write("\n\n")

    sys.stdout.write(f"Project dump written to: {output_file}\n")


def main() -> None:
    """
    CLI entrypoint.

    Executes CLI and writes project dump.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "directory",
        type=str,
        help="Project root directory",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="project_dump.txt.tmp",
    )

    args = parser.parse_args()

    dump_project(
        root=Path(args.directory),
        output_file=Path(args.output),
        patterns=DEFAULT_PATTERNS,
    )


if __name__ == "__main__":
    main()
