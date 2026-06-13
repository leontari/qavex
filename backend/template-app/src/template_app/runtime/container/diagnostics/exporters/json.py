from __future__ import annotations

import json
from typing import TYPE_CHECKING

from template_app.runtime.container.diagnostics.exporters.base import (
    DiagnosticsExporter,
)

if TYPE_CHECKING:
    from template_app.runtime.container.diagnostics.diagnostics import (
        ContainerSnapshot,
    )


class JsonExporter(DiagnosticsExporter):
    """JSON diagnostics exporter."""

    def export(self, snapshot: ContainerSnapshot) -> str:

        payload = {
            "registered_dependencies": snapshot.registered_dependencies,
            "active_scopes": snapshot.active_scopes,
            "singleton_instances": snapshot.singleton_instances,
            "namespaces": list(snapshot.namespaces),
            "graph": {
                "nodes": [str(node) for node in snapshot.graph.nodes],
                "edges": {
                    str(source): [str(target) for target in targets]
                    for source, targets in snapshot.graph.edges.items()
                },
            },
        }

        return json.dumps(payload, indent=2)
