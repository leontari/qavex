from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .diagnostics import ContainerSnapshot


def export_json(snapshot: ContainerSnapshot) -> str:
    """Export snapshot as JSON."""
    payload = {
        "dependencies": [
            {
                "contract": node.contract,
                "namespace": node.namespace,
                "scope": node.scope,
                "visibility": node.visibility,
            }
            for node in snapshot.graph.nodes
        ]
    }
    return json.dumps(payload, indent=4, sort_keys=True)


def export_dump(
    snapshot: ContainerSnapshot,
) -> str:
    """Human readable dump."""
    lines: list[str] = []
    lines.extend(
        (f"Dependencies: {snapshot.total_dependencies}", ""),
    )
    lines.extend(
        f"[{node.namespace}] {node.contract} ({node.scope}, {node.visibility})"
        for node in snapshot.graph.nodes
    )
    return "\n".join(lines)


def export_graph(snapshot: ContainerSnapshot) -> str:
    """GraphViz DOT export."""
    lines = ["digraph Container {"]
    lines.extend(
        f'"{node.namespace}" -> "{node.contract}"'
        for node in snapshot.graph.nodes
    )
    lines.append("}")
    return "\n".join(lines)
