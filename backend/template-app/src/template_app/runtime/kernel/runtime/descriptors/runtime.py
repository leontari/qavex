"""Runtime descriptor builder."""

from __future__ import annotations

from template_app.runtime.kernel.runtime.state import RuntimeState
from template_app.runtime.kernel.runtime.descriptors.models import (
    RuntimeDescriptor,
)


def build_runtime_descriptor(runtime: RuntimeState) -> RuntimeDescriptor:
    """
    Build runtime descriptor.

    Args:
        runtime:
            Runtime graph.

    Returns:
        Runtime descriptor.

    """
    lifecycle = runtime.lifecycle.registry

    return RuntimeDescriptor(
        modules=len(runtime.modules.registry.modules),
        transports=len(runtime.transports.manager.transports),
        startup_hooks=len(lifecycle.startup_hooks),
        shutdown_hooks=len(lifecycle.shutdown_hooks),
        readiness_probes=len(lifecycle.readiness_probes),
    )
