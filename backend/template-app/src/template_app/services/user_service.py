"""
Service layer for user-related operations.

This module defines the UserService class, which encapsulates all business
logic related to user management. The service layer acts as an abstraction
between the API routers and the repository layer, ensuring that routers
remain thin and focused on HTTP concerns only.
"""

from __future__ import annotations

from typing import Optional, List

from template_app.models.user import User, UserCreate, UserUpdate
from template_app.services.repositories.user_repository import UserRepository


class UserService:
    """Service class for managing user operations.

    This class provides high-level methods for creating, retrieving,
    updating, and deleting users. All persistence operations are delegated
    to the repository layer, allowing the service to remain independent
    of the underlying storage implementation.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with a user repository.

        Args:
            repository (UserRepository): Repository instance used for
                persistence operations.
        """
        self.repository = repository

    async def list_users(self) -> List[User]:
        """Return all registered users.

        Returns:
            List[User]: A list of all users stored in the system.
        """
        return await self.repository.list()

    async def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their unique identifier.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """
        return await self.repository.get(user_id)

    async def create_user(self, data: UserCreate) -> User:
        """Create a new user.

        Args:
            data (UserCreate): Payload containing user creation fields.

        Returns:
            User: The newly created user.
        """
        return await self.repository.create(data)

    async def update_user(
        self, user_id: int, data: UserUpdate
    ) -> Optional[User]:
        """Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (UserUpdate): Fields to update.

        Returns:
            Optional[User]: The updated user, or None if not found.
        """
        return await self.repository.update(user_id, data)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """
        return await self.repository.delete(user_id)
