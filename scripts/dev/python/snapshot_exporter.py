#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from template_app.runtime.kernel.bootstrap import bootstrap_kernel

##################
# FILESYSTEM GRAPH
##################


def build_file_graph(root: Path) -> dict[str, Any]:
    """
    Build filesystem graph snapshot.

    Returns:
        dict[str, Any]:
            File and directory structure summary with flat listings.

    """
    files: list[str] = []
    dirs: set[str] = set()

    for path in root.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue

        rel = str(path.relative_to(root))

        if path.is_dir():
            dirs.add(rel)
        else:
            files.append(rel)

    return {
        "root": str(root),
        "files_count": len(files),
        "dirs_count": len(dirs),
        "files": sorted(files),
        "dirs": sorted(dirs),
    }


##############
# IMPORT GRAPH
##############


def build_import_graph(root: Path) -> dict[str, list[str]]:
    """
    Build naive import graph (static scan).

    Returns:
        dict[str, list[str]]:
            Mapping file -> list of raw import lines.

    """
    import_graph: dict[str, list[str]] = {}

    for py_file in root.rglob("*.py"):
        if "__pycache__" in py_file.parts:
            continue

        rel = str(py_file.relative_to(root))

        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001, S112
            continue

        imports: list[str] = [
            line.strip()
            for line in content.splitlines()
            if line.startswith(("import ", "from "))
        ]

        import_graph[rel] = imports

    return import_graph


##############
# KERNEL GRAPH
##############


def build_kernel_graph(kernel: Any) -> dict[str, Any]:
    """
    Build runtime kernel graph snapshot.

    Returns:
        dict[str, Any]:
            Kernel runtime structure (modules, transports, lifecycle stats).

    """
    runtime = kernel.runtime

    return {
        "modules": [m.name for m in kernel.modules],
        "transports": [t.__class__.__name__ for t in kernel.transports],
        "lifecycle": {
            "startup_hooks": len(runtime.lifecycle.registry.startup_hooks),
            "shutdown_hooks": len(runtime.lifecycle.registry.shutdown_hooks),
        },
        "domains": {
            "lifecycle": type(runtime.lifecycle).__name__,
            "infrastructure": type(runtime.infrastructure).__name__,
            "messaging": type(runtime.messaging).__name__,
            "transports": type(runtime.transports).__name__,
            "modules": type(runtime.modules).__name__,
        },
    }


###################
# SNAPSHOT EXPORTER
###################


def export_snapshot(
    root: Path,
    output: Path,
    include_kernel: bool,  # noqa: FBT001
) -> None:
    """
    Export full architecture snapshot.

    Writes JSON snapshot to file system and emits status to stdout.

    Args:
        root:
            Project root directory to analyze.

        output:
            Output file path for JSON snapshot.

        include_kernel:
            Whether to include runtime kernel graph.

    """
    snapshot: dict[str, Any] = {
        "file_graph": build_file_graph(root),
        "import_graph": build_import_graph(root),
    }

    if include_kernel:
        kernel = bootstrap_kernel()
        snapshot["kernel_graph"] = build_kernel_graph(kernel)

    output.write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8",
    )

    sys.stdout.write(f"[snapshot-exporter] written: {output}\n")


######
# CLI
######


def main() -> None:
    """
    CLI entrypoint for architecture snapshot exporter.

    Exits after writing snapshot to disk.

    """
    parser = argparse.ArgumentParser(
        description="Architecture Snapshot Exporter (dev tool)",
    )

    parser.add_argument(
        "root",
        type=str,
        help="Target project root (e.g. backend/template-app/src)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="architecture_snapshot.json",
    )

    parser.add_argument(
        "--kernel",
        action="store_true",
        help="Include runtime kernel graph snapshot",
    )

    args = parser.parse_args()

    export_snapshot(
        root=Path(args.root),
        output=Path(args.output),
        include_kernel=args.kernel,
    )


if __name__ == "__main__":
    main()
