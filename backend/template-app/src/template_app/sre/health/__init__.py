"""
Enterprise health orchestration subsystem.

This package provides a production-grade health runtime designed for:

- Kubernetes readiness/liveness/startup probes
- async concurrent dependency checks
- cached probe execution
- background refresh scheduling
- dependency-aware orchestration
- degraded state propagation
- circuit breaker integration
- plugin-based extensibility

Main architecture layers:

- plugins:
    Health provider contracts and orchestration primitives.

- scheduler:
    Background execution and cached refresh engine.

- providers:
    Concrete health integrations such as PostgreSQL, Redis, Kafka,
    ClickHouse, external APIs, etc.

The subsystem is intentionally framework-like and designed to scale
across large microservice ecosystems.
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
from template_app.health.scheduler.loop import HealthScheduler

__all__ = [
    "HealthAggregator",
    "HealthCheckPlugin",
    "HealthCheckResult",
    "HealthDependencyGraph",
    "HealthPluginRegistry",
    "HealthScheduler",
    "HealthStatus",
    "RefreshPolicy",
]
