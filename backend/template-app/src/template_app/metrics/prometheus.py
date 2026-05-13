"""
Prometheus metrics registry.

This module contains Prometheus metric definitions used for
application observability and runtime monitoring.

The metrics defined here are intended for:
- Prometheus scraping
- Grafana dashboards
- Kubernetes monitoring
- container health analysis
- infrastructure observability
- runtime diagnostics

Metric categories:
- health metrics
- readiness metrics
- system resource metrics
- application runtime metrics

Design principles:
    - centralized metric definitions
    - reusable metric registry
    - cloud-native observability
    - Prometheus naming conventions
    - low-cardinality labels
    - production-safe instrumentation

Metric naming conventions:
    - snake_case metric names
    - descriptive metric suffixes
    - Prometheus-compatible naming
    - unit-aware metric identifiers

References:
    https://prometheus.io/docs/practices/naming/

"""

from __future__ import annotations

from prometheus_client import (
    Counter,
    Gauge,
)

# ============================================================================
# Health metrics
# ============================================================================

HEALTH_REQUESTS_TOTAL: Counter = Counter(
    name="health_requests_total",
    documentation="Total number of health endpoint requests.",
)

# ============================================================================
# Application readiness metrics
# ============================================================================

READINESS_STATUS: Gauge = Gauge(
    name="app_readiness_status",
    documentation=(
        "Application readiness status. "
        "1 indicates ready, 0 indicates not ready."
    ),
)

# ============================================================================
# System resource metrics
# ============================================================================

CPU_USAGE_PERCENT: Gauge = Gauge(
    name="app_cpu_usage_percent",
    documentation="Current application CPU usage percentage.",
)

MEMORY_USAGE_MB: Gauge = Gauge(
    name="app_memory_usage_mb",
    documentation="Current application memory usage in megabytes.",
)

# ============================================================================
# Exported metrics
# ============================================================================

__all__ = [
    "CPU_USAGE_PERCENT",
    "HEALTH_REQUESTS_TOTAL",
    "MEMORY_USAGE_MB",
    "READINESS_STATUS",
]
