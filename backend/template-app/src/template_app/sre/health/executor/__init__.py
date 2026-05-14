"""
Dependency graph execution engine for the health subsystem.

This package provides the runtime orchestration layer responsible for:

- executing health checks in dependency-aware order
- converting DAGs into execution layers
- applying execution policies (fail-fast, soft failure, skip rules)
- propagating degraded and unhealthy states
- coordinating async concurrent execution
- integrating with cached scheduler state

Core design principle:

    The executor does NOT know about infrastructure.
    It only knows about graph execution semantics.

Modules:

- graph_executor:
    Main dependency-aware execution engine.

- layer_builder:
    Converts dependency graph into execution layers.

- context:
    Shared execution state for runtime propagation.

- policies:
    Execution behavior configuration (skip, propagate, fail-fast).
"""

from __future__ import annotations

from template_app.health.executor.graph_executor import (
    DependencyGraphExecutor,
)
from template_app.health.executor.context import (
    ExecutionContext,
)
from template_app.health.executor.layer_builder import (
    LayerBuilder,
)
from template_app.health.executor.policies import (
    GraphExecutionPolicy,
    FailureMode,
    DegradedPropagationMode,
)

__all__ = [
    "DependencyGraphExecutor",
    "ExecutionContext",
    "LayerBuilder",
    "GraphExecutionPolicy",
    "FailureMode",
    "DegradedPropagationMode",
]
