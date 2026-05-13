"""
Application metrics package.

This package contains Prometheus-compatible metrics and observability
instrumentation used across the application.

Responsibilities:
- centralized metric definitions
- Prometheus instrumentation
- runtime observability
- infrastructure monitoring
- health and readiness metrics
- application performance metrics

Supported integrations:
- Prometheus
- Grafana
- Kubernetes monitoring stack
- OpenTelemetry collectors
- Loki
- Alertmanager

Design principles:
    - centralized observability
    - low-cardinality metrics
    - Prometheus naming conventions
    - cloud-native monitoring
    - production-safe instrumentation
    - reusable metric registry

Modules:
    prometheus:
        Prometheus metric definitions and instrumentation registry.
"""

from __future__ import annotations

from template_app.metrics.prometheus import (
    CPU_USAGE_PERCENT,
    HEALTH_REQUESTS_TOTAL,
    MEMORY_USAGE_MB,
    READINESS_STATUS,
)

__all__ = [
    "CPU_USAGE_PERCENT",
    "HEALTH_REQUESTS_TOTAL",
    "MEMORY_USAGE_MB",
    "READINESS_STATUS",
]
