"""
Health plugin system.

This package contains the core runtime primitives used by the health
orchestration subsystem:

- plugin contracts
- dependency graph resolution
- health aggregation
- registry management
- standardized result models

Plugins represent infrastructure dependencies and runtime subsystems such as:

- databases
- caches
- message brokers
- external APIs
- internal services
"""

from __future__ import annotations

from template_app.health.plugins.aggregator import HealthAggregator
from template_app.health.plugins.base import (
    HealthCheckPlugin,
    HealthCheckResult,
    HealthStatus,
    RefreshPolicy,
)
from template_app.health.plugins.dependency_graph import (
    HealthDependencyGraph,
)
from template_app.health.plugins.registry import (
    HealthPluginRegistry,
)

__all__ = [
    "HealthAggregator",
    "HealthCheckPlugin",
    "HealthCheckResult",
    "HealthDependencyGraph",
    "HealthPluginRegistry",
    "HealthStatus",
    "RefreshPolicy",
]
