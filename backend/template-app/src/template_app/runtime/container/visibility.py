from __future__ import annotations

from .exceptions import DependencyVisibilityError
from .namespace import DependencyNamespace, Namespace
from .types import DependencyVisibility


def enforce_visibility(
    *,
    owner: Namespace,
    requester: Namespace,
    visibility: DependencyVisibility,
) -> None:

    if visibility is DependencyVisibility.PUBLIC:
        return

    if visibility is DependencyVisibility.PRIVATE:
        if owner == requester:
            return

        msg = "Private dependency access denied"
        raise DependencyVisibilityError(msg)

    if visibility is DependencyVisibility.KERNEL:
        if requester.name == DependencyNamespace.KERNEL:
            return

        msg_0 = "Kernel dependency access denied"
        raise DependencyVisibilityError(msg_0)
