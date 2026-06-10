"""DI container exceptions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID


class DependencyError(RuntimeError):
    """Base dependency injection exception."""


class DependencyNotFoundError(DependencyError):
    """
    Raised when a dependency is not registered.

    Attributes:
        dependency_id:
            Identifier of the missing dependency.

    """

    dependency_id: DependencyID

    def __init__(self, dependency_id: DependencyID) -> None:  # noqa: D107
        self.dependency_id = dependency_id
        super().__init__(f"Dependency '{dependency_id}' is not registered.")


class DependencyAlreadyRegisteredError(DependencyError):
    """
    Raised when a dependency has already been registered.

    Attributes:
        dependency_id:
            Identifier of the registered dependency.

    """

    dependency_id: DependencyID

    def __init__(self, dependency_id: DependencyID) -> None:  # noqa: D107
        self.dependency_id = dependency_id
        super().__init__(
            f"Dependency '{dependency_id}' has already been registered."
        )


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
