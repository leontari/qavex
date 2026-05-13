"""
Prometheus runtime settings.

This module contains environment-driven Prometheus and metrics
configuration used for application observability and monitoring.

The settings defined here control:
- metrics exposition
- Prometheus integration
- instrumentation behavior
- monitoring namespaces
- runtime observability features

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes runtime injection
- CI/CD environment variables

Typical integrations:
- Prometheus
- Grafana
- Loki
- Alertmanager
- Kubernetes ServiceMonitor
- OpenTelemetry collectors

Security considerations:
    Metrics endpoints may expose sensitive operational information.

    Production deployments should:
    - restrict public access to metrics endpoints
    - use internal networking
    - protect observability infrastructure
    - avoid exposing infrastructure metadata publicly

Example:
    PROMETHEUS_ENABLED=true

Design principles:
    - strict typing
    - immutable runtime configuration
    - cloud-native observability
    - deployment portability
"""

from __future__ import annotations

from pydantic_settings import BaseSettings

from template_app.config.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class PrometheusSettings(BaseSettings):
    """
    Runtime Prometheus and metrics configuration.

    This settings model defines observability and metrics-related
    runtime configuration for Prometheus integration.

    Attributes:
        PROMETHEUS_ENABLED:
            Enables Prometheus metrics instrumentation.

        PROMETHEUS_NAMESPACE:
            Metrics namespace prefix used for exported metrics.

        PROMETHEUS_SUBSYSTEM:
            Metrics subsystem identifier used for grouping metrics.

        PROMETHEUS_MULTIPROC_DIR:
            Directory used for Prometheus multiprocess metrics mode.
    """

    PROMETHEUS_ENABLED: bool = True

    PROMETHEUS_NAMESPACE: str = "template_app"

    PROMETHEUS_SUBSYSTEM: str = "api"

    PROMETHEUS_MULTIPROC_DIR: str = "/tmp/prometheus"

    model_config = COMMON_SETTINGS_CONFIG
