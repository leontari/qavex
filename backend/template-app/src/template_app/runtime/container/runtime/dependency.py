from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic

from template_app.runtime.container.type_vars import T

if TYPE_CHECKING:
    from ..contracts import DependencyProvider
    from ..models import DependencyScope, DependencyVisibility, Namespace


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
class DependencyDescriptor(Generic[T]):
    """Dependency registration metadata."""

    ident: DependencyID
    provider: DependencyProvider[T]
    visibility: DependencyVisibility
    scope: DependencyScope
