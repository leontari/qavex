"""
Observability and runtime metrics endpoints.

/metrics
--------
Endpoint Responsibilities:
* Prometheus-compatible metrics endpoint
* Used by Grafana / Prometheus stack

/runtime
--------
Endpoint Responsibilities:
* Runtime observability
"""

from __future__ import annotations

import time

import psutil
from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from template_app.metrics.prometheus import cpu_usage_gauge, memory_usage_gauge

router = APIRouter(tags=["Observability"])

process = psutil.Process()

# @router.get("/metrics", summary="Runtime metrics")
# async def metrics() -> dict:
#     """Return basic runtime metrics for the service."""
#     return {
#         "uptime_seconds": time.time() - process.create_time(),
#         "cpu_percent": process.cpu_percent(interval=None),
#         "memory_rss_mb": process.memory_info().rss / 1024 / 1024,
#         "memory_vms_mb": process.memory_info().vms / 1024 / 1024,
#         "open_fds": process.num_fds() if hasattr(process, "num_fds") else None,
#         "threads": process.num_threads(),
#     }


@router.get("/runtime", summary="Runtime metrics")
async def runtime_metrics() -> dict:
    """
    Return runtime process metrics.

    Returns:
        Runtime statistics.

    """
    cpu_percent = process.cpu_percent(interval=None)
    memory_rss_mb = process.memory_info().rss / 1024 / 1024

    cpu_usage_gauge.set(cpu_percent)
    memory_usage_gauge.set(memory_rss_mb)

    return {
        "uptime_seconds": time.time() - process.create_time(),
        "cpu_percent": cpu_percent,
        "memory_rss_mb": memory_rss_mb,
        "memory_vms_mb": process.memory_info().vms / 1024 / 1024,
        "open_fds": (
            process.num_fds() if hasattr(process, "num_fds") else None
        ),
        "threads": process.num_threads(),
    }


@router.get("/metrics", summary="Prometheus metrics")
def metrics() -> Response:
    """
    Return Prometheus metrics.

    Returns:
        Prometheus metrics response.

    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
