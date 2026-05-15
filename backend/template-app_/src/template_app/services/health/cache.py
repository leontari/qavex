"""
TTL cache for readiness responses.

readiness cache (anti-DDOS readiness)
"""

from __future__ import annotations

import time
from typing import Any


class TTLCache:
    """Simple in-memory TTL cache."""

    def __init__(self, ttl: float = 5.0):
        self.ttl = ttl
        self._value: Any = None
        self._expires = 0

    def get(self):
        """Return cached value if not expired."""
        if time.time() < self._expires:
            return self._value
        return None

    def set(self, value: Any):
        """Store value in cache"""
        self._value = value
        self._expires = time.time() + self.ttl


readiness_cache = TTLCache(ttl=5.0)
