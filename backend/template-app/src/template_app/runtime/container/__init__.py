"""Dependency injection system."""

from __future__ import annotations

from .container import Container
from .models import DependencyScope, DependencyVisibility, Namespace

__version__ = "3.6.0"

__all__ = (
    "Container",
    "DependencyScope",
    "DependencyVisibility",
    "Namespace",
    "__version__",
)
