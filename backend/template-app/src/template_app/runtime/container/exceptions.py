"""DI exceptions."""

from __future__ import annotations


class DependencyError(RuntimeError):
    """Base dependency injection exception."""


class DependencyNotFoundError(DependencyError):
    """Dependency not found."""


class DependencyAlreadyRegisteredError(DependencyError):
    """Dependency already registered."""


class DependencyNamespaceError(DependencyError):
    """Namespace violation."""


class DependencyVisibilityError(DependencyError):
    """Visibility violation."""


class InvalidProviderError(DependencyError):
    """Invalid provider registration."""


class AsyncDependencyError(DependencyError):
    """Async dependency resolved synchronously."""


class ScopeRequiredError(DependencyError):
    """Scoped dependency resolved without scope."""


class DependencyCycleError(DependencyError):
    """Dependency cycle detected."""
