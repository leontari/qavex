"""DI container exceptions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import DependencyID
    from template_app.runtime.container.models.scope import (
        DependencyScope,
        ScopeID,
    )


class ContainerError(RuntimeError):
    """Base dependency injection exception."""


class DependencyNotFoundError(ContainerError):
    """
    Raised when a dependency is not registered.

    Attributes:
        dependency_id:
            Identifier of the missing dependency.

    """

    def __init__(self, dependency_id: DependencyID) -> None:  # noqa: D107
        self.dependency_id = dependency_id
        super().__init__(f"Dependency '{dependency_id}' is not registered.")


class DependencyAlreadyRegisteredError(ContainerError):
    """
    Raised when a dependency has already been registered.

    Attributes:
        dependency_id:
            Identifier of the registered dependency.

    """

    def __init__(self, dependency_id: DependencyID) -> None:  # noqa: D107
        self.dependency_id = dependency_id
        super().__init__(
            f"Dependency '{dependency_id}' has already been registered."
        )


class ScopeNotFoundError(ContainerError):
    """
    Scope not found error.

    Attributes:
        scope_id:
            Identifier of the scope

    """

    def __init__(self, scope_id: ScopeID) -> None:  # noqa: D107
        self.scope_id = scope_id
        super().__init__(f"Scope {scope_id} not found.")


class ScopeClosedError(ContainerError):
    """
    Scope is no longer active.

    Attributes:
        scope_id:
            Identifier of the scope

    """

    def __init__(self, scope_id: ScopeID) -> None:  # noqa: D107
        self.scope_id = scope_id
        super().__init__(f"Scope '{scope_id} is closed.")


class ScopeRequiredError(ContainerError):
    """
    Scoped dependency resolved outside scope.

    Attributes:
        dependency_id:
            Identifier of the dependency.

    """

    def __init__(self, dependency_id: DependencyID) -> None:  # noqa: D107
        self.dependency_id = dependency_id
        super().__init__(
            f"Dependency '{dependency_id}' requires active scope."
        )


class UnsupportedScopeError(ContainerError):
    """
    Unsupported dependency lifetime.

    Attributes:
        scope:
            dependency lifetime policy.

    """

    def __init__(self, scope: DependencyScope) -> None:  # noqa: D107
        self.scope = scope
        super().__init__(f"Unsupported dependency scope: {scope}")


class DependencyNamespaceError(ContainerError):
    """Namespace violation error."""


class InvalidContractError(ContainerError):
    """Provider contract error."""


class DependencyVisibilityError(ContainerError):
    """Visibility violation error."""


class InvalidProviderError(ContainerError):
    """Invalid provider registration."""


class AsyncDependencyError(ContainerError):
    """Sync resolve attempted on async dependency."""


class DependencyCycleError(ContainerError):
    """Circular dependency detected during resolution."""

    def __init__(  # noqa: D107
        self,
        stack: tuple[DependencyID, ...],
        dependency_id: DependencyID,
    ) -> None:

        self.stack = stack
        self.dependency_id = dependency_id
        self.cycle = (*stack, dependency_id)

        super().__init__(f"Circular dependency detected: {self.chain}")

    @property
    def chain(self) -> str:
        """
        Formatted dependency cycle chain.

        Returns:
            Human-readable dependency chain.

        """
        return " -> ".join(map(str, self.cycle))

    @property
    def cycle_length(self) -> int:
        """
        Cycle size.

        Returns:
            Number of dependencies in cycle.

        """
        return len(self.cycle)


class DependencyGraphError(ContainerError):
    """Dependency graph validation failed."""


class PluginValidationError(ContainerError):
    """Plugin declaration validation failed."""


class NamespaceIsolationError(ContainerError):
    """Plugin namespace isolation violation."""
