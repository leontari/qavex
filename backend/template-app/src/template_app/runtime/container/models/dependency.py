from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.scope import DependencyScope
if TYPE_CHECKING:
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.container.models.namespace import Namespace
    from template_app.runtime.container.models.visibility import (
        DependencyVisibility,
    )


@dataclass(frozen=True, slots=True)
class DependencyID:
    """Unique dependency identifier."""

    namespace: Namespace
    contract: type[Any]

    def __str__(self) -> str:
        """
        Return a diagnostic message.

        Returns:
            a human-readable string representation of the DependencyID object

        """
        return (
            f"{self.namespace.name}:"
            f"{self.contract.__module__}."
            f"{self.contract.__qualname__}"
        )


@dataclass(frozen=True, slots=True)
class DependencyDescriptor:
    """Dependency registration metadata."""

    ident: DependencyID
    provider: DependencyProvider[type[Any]]
    visibility: DependencyVisibility
    scope: DependencyScope
