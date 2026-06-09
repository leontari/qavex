from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.graph.diagnostics import (
        ContainerSnapshot,
    )


def export_json(snapshot: ContainerSnapshot) -> str:
    """Export snapshot as JSON."""
    payload = {
        "dependencies": [
            {
                "contract": node.contract.__name__,
                "namespace": node.namespace.name,
                "scope": node.scope.value,
                "visibility": node.visibility.value,
            }
            for node in snapshot.graph.nodes.values()
        ],
        "edges": [
            {
                "source": edge.source.__name__,
                "target": edge.target.__name__,
                "scope": edge.scope_ide,
            }
            for edge in snapshot.graph.edges
        ],
    }
    return json.dumps(
        payload,
        indent=4,
        sort_keys=True,
    )


def export_dump(
    snapshot: ContainerSnapshot,
) -> str:
    """
    Human-readable container dump.
    """

    lines: list[str] = []

    lines.append(
        f"Dependencies: {snapshot.total_dependencies}",
    )
    lines.append(
        f"Edges: {snapshot.total_edges}",
    )
    lines.append("")

    grouped: dict[str, list[str]] = {}

    for node in snapshot.graph.nodes.values():
        grouped.setdefault(
            node.namespace.name,
            [],
        ).append(
            (f"{node.contract.__name__} [{node.scope.value}]"),
        )

    for namespace in sorted(grouped):
        lines.append(namespace)

        for dependency in sorted(grouped[namespace]):
            lines.append(f"  └── {dependency}")

        lines.append("")

    return "\n".join(lines)


def export_graphviz(
    snapshot: ContainerSnapshot,
) -> str:
    """
    Export graph as GraphViz DOT.
    """

    lines = [
        "digraph DependencyGraph {",
    ]

    for node in snapshot.graph.nodes.values():
        lines.append(
            (
                f'"{node.contract.__name__}" '
                f'[label="{node.contract.__name__}\\n'
                f'{node.namespace.name}"]'
            ),
        )

    for edge in snapshot.graph.edges:
        lines.append(
            (f'"{edge.source.__name__}" -> "{edge.target.__name__}"'),
        )

    lines.append("}")

    return "\n".join(lines)
