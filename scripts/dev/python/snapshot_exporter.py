from __future__ import annotations

import argparse
import ast
import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from template_app.runtime.kernel.bootstrap import bootstrap_kernel

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel

######################
# ArchitectureSnapshot
######################


@dataclass(slots=True)
class ArchitectureSnapshot:
    "Snapshot of the project architecture."

    filesystem: dict[str, Any]

    import_graph: dict[str, Any]
    dependency_graph: dict[str, Any]

    runtime_graph: dict[str, Any]

    transport_graph: dict[str, Any]
    module_graph: dict[str, Any]

    pytest_fixture_graph: dict[str, Any]

    lifecycle_dag: dict[str, Any]


##########################
# IMPORT GRAPH (AST-based)
##########################


def build_import_graph(root: Path) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    for file in root.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except Exception:
            continue

        imports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        graph[str(file.relative_to(root))] = sorted(set(imports))

    return graph


##############################
# RUNTIME GRAPH (kernel state)
##############################


def build_runtime_graph(kernel: RuntimeKernel) -> dict[str, object]:
    return {
        "modules": len(kernel.modules),
        "transports": len(kernel.transports),
        "has_lifecycle": kernel.lifecycle is not None,
        "has_messaging": kernel.messaging is not None,
        "has_infra": kernel.infrastructure is not None,
    }


#################
# TRANSPORT GRAPH
#################


def build_transport_graph(kernel: RuntimeKernel) -> dict[str, object]:
    return {
        "count": len(kernel.transports),
        "types": [type(t).__name__ for t in kernel.transports],
        "names": [getattr(t, "name", None) for t in kernel.transports],
    }


##############
# MODULE GRAPH
##############


def build_module_graph(kernel: RuntimeKernel) -> dict[str, object]:
    return {
        "count": len(kernel.modules),
        "modules": [
            {
                "name": m.name,
                "version": getattr(m, "version", None),
            }
            for m in kernel.modules
        ],
    }


######################
# PYTEST FIXTURE GRAPH
######################


def build_pytest_fixture_graph() -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    for name, obj in pytest.FIXTURES.items():  # internal pytest registry
        try:
            sig = inspect.signature(obj)
            graph[name] = list(sig.parameters.keys())
        except Exception:
            graph[name] = []

    return graph


##################################
# DEPENDENCY GRAPH (kernel wiring)
##################################


def build_dependency_graph(kernel: RuntimeKernel) -> dict[str, object]:
    return {
        "kernel": {
            "lifecycle": id(kernel.lifecycle),
            "messaging": id(kernel.messaging),
            "infra": id(kernel.infrastructure),
            "transports": id(kernel.transport_manager),
        }
    }


############################
# LIFECYCLE DAG (core value)
############################


def build_lifecycle_dag(kernel: RuntimeKernel) -> dict[str, list[str]]:
    registry = kernel.runtime.lifecycle.registry

    return {
        "startup": [
            hook.__name__ for hook in getattr(registry, "startup_hooks", [])
        ],
        "shutdown": [
            hook.__name__ for hook in getattr(registry, "shutdown_hooks", [])
        ],
        "readiness": [
            probe.__name__
            for probe in getattr(registry, "readiness_probes", [])
        ],
    }


def export_architecture_snapshot(
    root: Path,
    kernel: RuntimeKernel | None,
    output: Path,
) -> None:

    snapshot = {
        "filesystem": {},
        "import_graph": build_import_graph(root),
        "dependency_graph": {},
        "runtime_graph": {},
        "transport_graph": {},
        "module_graph": {},
        "pytest_fixture_graph": build_pytest_fixture_graph(),
        "lifecycle_dag": {},
    }

    if kernel:
        snapshot["runtime_graph"] = build_runtime_graph(kernel)
        snapshot["transport_graph"] = build_transport_graph(kernel)
        snapshot["module_graph"] = build_module_graph(kernel)
        snapshot["dependency_graph"] = build_dependency_graph(kernel)
        snapshot["lifecycle_dag"] = build_lifecycle_dag(kernel)

    output.write_text(str(snapshot), encoding="utf-8")

    sys.stdout.write(f"[architecture snapshot] → {output}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="architecture-snapshot",
        description="Export kernel + code architecture snapshot",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    snapshot = sub.add_parser(
        "snapshot",
        help="Export architecture snapshot",
    )

    snapshot.add_argument(
        "--root",
        type=str,
        default=".",
        help="Project root directory",
    )

    snapshot.add_argument(
        "--output",
        type=str,
        default="architecture_snapshot.json",
        help="Output file",
    )

    snapshot.add_argument(
        "--kernel",
        action="store_true",
        help="Include runtime kernel graph",
    )

    return parser


def cmd_snapshot(args: argparse.Namespace) -> None:
    kernel = bootstrap_kernel() if args.kernel else None

    export_architecture_snapshot(
        root=Path(args.root),
        kernel=kernel,
        output=Path(args.output),
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "snapshot":
        cmd_snapshot(args)


if __name__ == "__main__":
    main()
