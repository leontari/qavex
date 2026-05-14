"""
HTTP routes for runtime health orchestration.

This module exposes Kubernetes-compatible endpoints for:

- liveness probes
- readiness probes
- aggregated runtime health

The endpoints are intentionally cache-driven and do not execute
infrastructure checks during HTTP requests.

All health state is retrieved from the background scheduler cache.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette import status

from template_app.health.plugins.base import (
    HealthStatus,
)

if TYPE_CHECKING:
    from template_app.health.service import (
        HealthService,
    )

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


def get_health_service(
    request: Request,
) -> HealthService:
    """
    Retrieve runtime health service from application state.

    Args:
        request:
            FastAPI request instance.

    Returns:
        HealthService:
            Runtime health orchestration service.

    """
    return request.app.state.health_service


@router.get(
    "/live",
    summary="Kubernetes liveness probe",
)
async def live(
    request: Request,
) -> JSONResponse:
    """
    Runtime liveness probe.

    The liveness probe verifies only that the runtime itself remains
    responsive and operational.

    Infrastructure dependencies such as databases or caches are NOT
    validated here.

    Args:
        request:
            FastAPI request instance.

    Returns:
        JSONResponse:
            Liveness probe response.

    """
    service = get_health_service(request)

    result = service.get_liveness()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": result.status,
            "timestamp": result.timestamp,
        },
    )


@router.get(
    "/ready",
    summary="Kubernetes readiness probe",
)
async def ready(
    request: Request,
) -> JSONResponse:
    """
    Runtime readiness probe.

    The readiness probe validates runtime dependency availability using
    cached scheduler-managed health state.

    Returns:
        HTTP 200:
            Runtime is healthy or degraded.

        HTTP 503:
            Runtime is unavailable.

    """
    service = get_health_service(request)

    readiness = service.get_readiness()

    status_code = (
        status.HTTP_503_SERVICE_UNAVAILABLE
        if readiness.status == HealthStatus.UNHEALTHY
        else status.HTTP_200_OK
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "status": readiness.status,
            "generated_at": readiness.generated_at,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status,
                    "latency_ms": check.latency_ms,
                    "details": check.details,
                    "error": check.error,
                }
                for check in readiness.checks
            ],
        },
    )


@router.get(
    "",
    summary="Aggregated runtime health",
)
async def health(
    request: Request,
) -> JSONResponse:
    """
    Aggregate runtime health endpoint.

    This endpoint provides detailed runtime health state including all
    registered infrastructure dependencies and subsystem checks.

    Returns:
        JSONResponse:
            Aggregated runtime health state.

    """
    service = get_health_service(request)

    readiness = service.get_readiness()

    status_code = (
        status.HTTP_503_SERVICE_UNAVAILABLE
        if readiness.status == HealthStatus.UNHEALTHY
        else status.HTTP_200_OK
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "status": readiness.status,
            "generated_at": readiness.generated_at,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status,
                    "latency_ms": check.latency_ms,
                    "details": check.details,
                    "error": check.error,
                }
                for check in readiness.checks
            ],
        },
    )
