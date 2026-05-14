"""
Public API schemas for the health subsystem.

This module defines external-facing response models for:

- liveness probes
- readiness probes
- full aggregated health state
- plugin-level diagnostic output

These schemas are designed to be:

- Kubernetes-compatible
- stable across versions
- transport-layer safe (no internal Python objects exposed)
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from template_app.health.plugins.base import HealthStatus


class HealthCheckItemSchema(BaseModel):
    """
    Single plugin health check representation.

    This schema is exposed via /health endpoints.
    """

    name: str = Field(..., description="Plugin name")

    status: HealthStatus = Field(..., description="Health status")

    latency_ms: float = Field(..., description="Execution latency in ms")

    details: dict | None = Field(
        default=None,
        description="Optional structured diagnostics payload",
    )

    error: str | None = Field(
        default=None,
        description="Optional error message if check failed",
    )


class AggregatedHealthSchema(BaseModel):
    """
    Aggregated system health response.

    Used by readiness and full health endpoints.
    """

    status: HealthStatus = Field(..., description="Overall system health")

    generated_at: float = Field(
        ...,
        description="Unix timestamp of aggregation",
    )

    checks: list[HealthCheckItemSchema] = Field(
        default_factory=list,
        description="List of individual health checks",
    )


class LivenessSchema(BaseModel):
    """
    Liveness probe schema.

    Represents minimal runtime health state.
    """

    status: HealthStatus = Field(
        ...,
        description="Runtime liveness status",
    )

    timestamp: float = Field(
        ...,
        description="Evaluation timestamp",
    )


class StartupSchema(BaseModel):
    """
    Startup probe schema.

    Used during Kubernetes startupProbe phase.
    """

    status: HealthStatus = Field(
        ...,
        description="Startup readiness status",
    )

    ready: bool = Field(
        ...,
        description="Whether application is fully initialized",
    )
