"""
Observability components for the service.

Includes health checks, Prometheus metrics endpoints, and
router definitions for exposing operational diagnostics.
"""

from __future__ import annotations

from template_app.api.health.health import router as health_router
from template_app.api.health.live import router as live_router
from template_app.api.health.metrics import router as metrics_router
from template_app.api.health.ready import router as ready_router

__all__ = [
    "health_router",
    "live_router",
    "metrics_router",
    "ready_router",
]
