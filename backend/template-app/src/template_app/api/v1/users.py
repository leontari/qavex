"""
User-related API endpoints.

This module defines operations for managing users, including retrieval,
creation, update, and deletion. All endpoints are mounted under the
`/users` prefix by the versioned router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from template_app.core_.dependencies import get_user_service
from template_app.models_.user import User, UserCreate, UserUpdate
from template_app.services.user_service import UserService

router = APIRouter()


@router.get("/", summary="List all users")
async def list_users(
    service: UserService = Depends(get_user_service),
) -> list[User]:
    """Return a list of all registered users."""
    return await service.list_users()


@router.get("/{user_id}", summary="Get a user by ID")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> User:
    """Retrieve a user by ID."""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", summary="Create a new user")
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> User:
    """Create a new user."""
    return await service.create_user(data)


@router.put("/{user_id}", summary="Update a user")
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> User:
    """Update an existing user."""
    updated = await service.update_user(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", summary="Delete a user")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict:
    """Delete a user by ID."""
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
