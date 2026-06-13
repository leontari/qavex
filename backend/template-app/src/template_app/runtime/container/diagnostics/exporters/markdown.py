from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.container.diagnostics.exporters.base import (
    DiagnosticsExporter,
)

if TYPE_CHECKING:
    from template_app.runtime.container.diagnostics.snapshot import (
        ContainerSnapshot,
    )


class MarkdownExporter(DiagnosticsExporter):
    """Markdown diagnostics exporter."""

    def export(self, snapshot: ContainerSnapshot) -> str:

        return f"""
# Container Diagnostics

## Summary

| Metric | Value |
|---------|---------|
| Dependencies | {snapshot.registered_dependencies} |
| Active scopes | {snapshot.active_scopes} |
| Singletons | {snapshot.singleton_instances} |

## Namespaces

{chr(10).join(f"- {ns}" for ns in snapshot.namespaces)}
""".strip()
