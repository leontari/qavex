from __future__ import annotations

from typing import TYPE_CHECKING

from .base import DiagnosticsExporter

if TYPE_CHECKING:
    from ..snapshot import ContainerSnapshot


class TextExporter(DiagnosticsExporter):
    """Plain text diagnostics exporter."""

    def export(self, snapshot: ContainerSnapshot) -> str:

        lines = [
            "Container Diagnostics",
            "====================",
            "",
            f"Dependencies : {snapshot.registered_dependencies}",
            f"Namespaces   : {len(snapshot.namespaces)}",
            f"Scopes       : {snapshot.active_scopes}",
            f"Singletons   : {snapshot.singleton_instances}",
            "",
            "Namespaces",
            "----------",
        ]

        lines.extend(snapshot.namespaces)

        return "\n".join(lines)
