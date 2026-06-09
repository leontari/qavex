"""Visibility rules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import (
    DependencyVisibilityError,
)
from template_app.runtime.container.models.visibility import (
    DependencyVisibility,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.namespace import Namespace


def enforce_visibility(
    *,
    owner: Namespace,
    requester: Namespace,
    visibility: DependencyVisibility,
) -> None:
    """
    Validate runtime visibility.

    Rules:
        1. PUBLIC -> allowed everywhere
        2. PRIVATE -> same namespace only
        3. KERNEL -> only kernel OR kernel-scoped boundary access

    """
    # FAST PATH
    if visibility is DependencyVisibility.PUBLIC:
        return

    # PRIVATE: strict namespace boundary
    if visibility is DependencyVisibility.PRIVATE:
        if owner != requester:
            msg = (
                f"PRIVATE violation: "
                f"{requester.name} cannot access {owner.name}"
            )
            raise DependencyVisibilityError(msg)
        return
