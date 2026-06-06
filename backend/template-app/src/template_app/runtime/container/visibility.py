from __future__ import annotations

from typing import TYPE_CHECKING

from .exceptions import (
    DependencyNamespaceError,
    DependencyVisibilityError,
)
from .types import DependencyVisibility

if TYPE_CHECKING:
    from .namespace import Namespace


def enforce_visibility(
    *,
    owner: Namespace,
    requester: Namespace,
    visibility: DependencyVisibility,
) -> None:
    """Validate dependency access."""
    if visibility is DependencyVisibility.PUBLIC:
        return

    if visibility is DependencyVisibility.PRIVATE:
        if owner != requester:
            msg = (
                f"Namespace '{requester}' "
                f"cannot access private dependency "
                f"from '{owner}'"
            )
            raise DependencyVisibilityError(msg)

        return

    if (
        visibility is DependencyVisibility.KERNEL
        and requester.name != "kernel"
    ):
        msg = f"Dependency from '{owner}' is available only for kernel"
        raise DependencyNamespaceError(msg)

    return
