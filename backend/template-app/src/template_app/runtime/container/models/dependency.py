from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.container.models.namespace import Namespace
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


@dataclass(frozen=True, slots=True)
class DependencyDescriptor:
    """Dependency registration metadata."""

    provider: DependencyProvider[type[Any]]
    visibility: DependencyVisibility
