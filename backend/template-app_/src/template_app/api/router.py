"""
Root API router configuration for the Template App service.

This module defines the top-level API router and mounts versioned
sub-routers for different functional domains. Each versioned router
is responsible for grouping related endpoints and ensuring backward
compatibility as the API evolves.
"""

from __future__ import annotations

from fastapi import APIRouter

from template_app.api.v1.router import api_v1_router

# Root API router (no prefix here!)
api_router = APIRouter()


# Mount versioned API routers
api_router.include_router(api_v1_router, prefix="/v1")
