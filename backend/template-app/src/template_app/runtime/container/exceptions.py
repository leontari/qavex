"""DI container exceptions."""

from __future__ import annotations


class DependencyError(RuntimeError):
    """Base dependency injection exception."""


class DependencyNotFoundError(DependencyError):
    """Dependency is not registered."""


class DependencyAlreadyRegisteredError(DependencyError):
    """Dependency already exists."""


class DependencyNamespaceError(DependencyError):
    """Namespace violation error."""


class DependencyVisibilityError(DependencyError):
    """Visibility violation error."""


class InvalidProviderError(DependencyError):
    """Invalid provider registration."""


class AsyncDependencyError(DependencyError):
    """Sync resolve attempted on async dependency."""


class ScopeRequiredError(DependencyError):
    """Scoped dependency resolved outside scope."""


class DependencyCycleError(DependencyError):
    """Dependency cycle detected."""


class DependencyGraphError(DependencyError):
    """Dependency graph validation failed."""


class PluginValidationError(DependencyError):
    """Plugin declaration validation failed."""


class NamespaceIsolationError(DependencyError):
    """Plugin namespace isolation violation."""
