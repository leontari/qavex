"""
Shared response models.

This module defines generic response models used across multiple
endpoints, such as health checks, status messages, and standardized
API responses.
"""

from __future__ import annotations

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Represents a simple message response.

    Attributes:
        message (str): Human-readable message.
    """

    message: str


class HealthResponse(BaseModel):
    """Represents a health check response.

    Attributes:
        status (str): Service status indicator.
        version (str): Current application version.
    """

    status: str
    version: str
