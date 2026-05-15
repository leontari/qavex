"""
Readiness probe endpoint.

Checks whether the application is ready to accept traffic.
Checks external dependencies with caching + timeout safety.

It MAY depend on external services like databases, caches, queues, etc.

/ready
------
Endpoint Responsibilities:
* Is the application ready to serve traffic?
Checks:
* Database connectivity
* Redis availability
* External APIs
* Database migrations status
"""

from __future__ import annotations

from fastapi import APIRouter

from template_app.services.health.cache import readiness_cache
from template_app.services.health.status import get_readiness_state

router = APIRouter(tags=["Health"])

#
# async def check_database() -> bool:
#     """
#     Simulate DB check.
#
#     Replace with real DB ping logic.
#
#     Returns:
#         True if database is reachable, otherwise False
#
#     """
#     return True
#
#
# async def check_redis() -> bool:
#     """
#     Simulate Redis check.
#
#     Replace with real Redis ping logic.
#
#     Returns:
#         True if Redis is reachable, otherwise False
#
#     """
#     return True


@router.get("/ready", summary="Readiness probe")
async def ready() -> dict:
    """
    Return readiness state.

    Returns:
        Application readiness status.

    """
    cached = readiness_cache.get()

    if cached:
        return cached

    state = await get_readiness_state()
    readiness_cache.set(state)

    return state
