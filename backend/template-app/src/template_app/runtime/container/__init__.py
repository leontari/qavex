"""Dependency injection system."""

from __future__ import annotations

from .container import Container
from .contracts import AsyncDisposable, DependencyProvider, DependencyResolver
from .models import (
    DependencyScope,
    DependencyVisibility,
    Namespace,
    Namespaces,
)
from .providers import FactoryProvider
from .type_aliases import Factory

__version__ = "3.7.1"

__all__ = (
    "AsyncDisposable",
    "Container",
    "DependencyProvider",
    "DependencyResolver",
    "DependencyScope",
    "DependencyVisibility",
    "Factory",
    "FactoryProvider",
    "Namespace",
    "Namespaces",
    "__version__",
)
