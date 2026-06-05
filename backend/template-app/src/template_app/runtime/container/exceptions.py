from __future__ import annotations


class DependencyError(RuntimeError):
    """Base DI exception."""


class DependencyNotFoundError(DependencyError):
    """Dependency not found."""


class DependencyAlreadyRegisteredError(DependencyError):
    """Dependency already registered."""


class DependencyVisibilityError(DependencyError):
    """Visibility violation."""


class DependencyScopeError(DependencyError):
    """Visibility violation."""
