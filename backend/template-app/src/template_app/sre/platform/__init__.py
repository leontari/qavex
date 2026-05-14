"""
Platform runtime layer.

This package contains the runtime orchestration platform responsible for:

- control plane execution
- runtime state synthesis
- reconciliation loops
- event-driven orchestration
- dependency graph execution
- observability runtime integration

The platform layer is the operational kernel of the service runtime.

Architecture:

    infrastructure
        ↓
    health graph
        ↓
    decision engine
        ↓
    runtime state engine
        ↓
    event bus
        ↓
    reconciliation loop
        ↓
    runtime actions
        ↓
    kubernetes / sre / observability systems
"""

from __future__ import annotations

from template_app.platform.bootstrap import (
    bootstrap_platform,
)
from template_app.platform.runtime import (
    PlatformRuntime,
)

__all__ = [
    "PlatformRuntime",
    "bootstrap_platform",
]
