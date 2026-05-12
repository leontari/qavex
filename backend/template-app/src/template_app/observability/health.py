"""
Health check endpoints.

This module provides liveness and readiness probes
for monitoring and orchestration systems.
"""

from __future__ import annotations

from fastapi import APIRouter

from template_app.config.app import config

router = APIRouter()


@router.get("/health", summary="Liveness probe")
async def health() -> dict[str, str | None]:
    """
    Return liveness probe result.

    Returns:
        Application status, version, and commit hash.

    """
    return {
        "status": "ok",
        "version": config.APP_VERSION,
        "commit": config.APP_COMMIT_SHA,
    }
