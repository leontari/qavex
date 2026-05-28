"""Runtime graph inspector."""

from __future__ import annotations


class RuntimeGraphInspector:
    """
    Runtime graph inspector.

    Responsibilities:
        - runtime graph inspection
        - diagnostics rendering
        - runtime topology rendering
    """

    @staticmethod
    def inspect(runtime) -> dict[str, object]:
        """
        Inspect runtime graph.

        Args:
            runtime:
                Runtime graph.

        Returns:
            Runtime inspection snapshot.

        """
        return {
            "modules": len(runtime.modules.registry.modules),
            "transports": len(runtime.transports.manager.transports),
            "startup_hooks": len(
                runtime.lifecycle.registry.startup_hooks,
            ),
            "shutdown_hooks": len(
                runtime.lifecycle.registry.shutdown_hooks,
            ),
            "readiness_probes": len(
                runtime.lifecycle.registry.readiness_probes,
            ),
        }
