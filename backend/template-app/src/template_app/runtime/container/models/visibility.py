from __future__ import annotations

from enum import StrEnum


class DependencyVisibility(StrEnum):
    """Dependency visibility policy."""

    PUBLIC = "public"  # available to all
    PRIVATE = "private"  # available only for namespace members
