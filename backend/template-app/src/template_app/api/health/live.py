"""
Liveness probe endpoint.

This endpoint verifies that the application process
is alive and not deadlocked.

No dependencies allowed. It should stay as simple as possible.

/live
------
Endpoint Responsibilities:
* Is the application alive?
* Has no external dependencies
* Used by container restart mechanisms (liveness probes)
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/live", summary="Liveness probe")
async def live() -> dict[str, str]:
    """
    Return liveness state.

    Returns:
        Application liveness status.

    """
    return {
        "status": "alive",
    }
