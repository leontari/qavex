"""
Version 1 API router.

This module aggregates all domain-specific routers for API v1 and exposes
them under a unified versioned namespace. The version prefix is applied
by the root API router to avoid duplication and ensure consistent routing.
"""

from __future__ import annotations

from fastapi import APIRouter

# from template_app.api.v1.auth import router as auth_router
from template_app.api.v1.users import router as users_router

# No prefix here — it is applied in the root API router
api_v1_router = APIRouter()

api_v1_router.include_router(users_router, prefix="/users", tags=["users"])
# api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
