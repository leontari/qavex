"""
Deep health diagnostics endpoint.

/health
-------
Endpoint Responsibilities:
* Deep diagnostic endpoint
* Aggregated dependency state
* Internal system health snapshot
"""

from __future__ import annotations

from fastapi import APIRouter

from template_app.services.health.status import get_full_health

router = APIRouter()


@router.get("/health", summary="Deep health diagnostics")
async def health() -> dict:
    """
    Return detailed system health.

    Returns:
        Full health diagnostics snapshot.

    """
    return await get_full_health()
