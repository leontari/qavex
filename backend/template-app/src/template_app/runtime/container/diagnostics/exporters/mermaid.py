from template_app.runtime.container.diagnostics.exporters.base import (
    DiagnosticsExporter,
)
from template_app.runtime.container.diagnostics.snapshot import (
    ContainerSnapshot,
)


class MermaidExporter(DiagnosticsExporter):
    """Mermaid graph exporter."""

    def export(self, snapshot: ContainerSnapshot) -> str:
        lines = ["graph TD"]
        for source, targets in snapshot.graph.edges.items():
            source_name = source.contract.__name__

            for target in targets:
                target_name = target.contract.__name__
                lines.append(f"    {source_name} --> {target_name}")

        return "\n".join(lines)


class NamespaceMermaidExporter:
    """Mermaid namespace exporter."""

    def export(self, snapshot: ContainerSnapshot) -> str: ...
