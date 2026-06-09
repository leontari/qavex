from __future__ import annotations

import pytest

from template_app.runtime.container.exceptions import (
    DependencyVisibilityError,
)
from template_app.runtime.container.runtime.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)
from template_app.runtime.container.types import (
    DependencyVisibility,
)


class InternalService:
    pass


def test_private_dependency_cannot_be_resolved() -> None:
    manager = DependencyManager()

    manager.register(
        InternalService,
        SingletonProvider(
            lambda _: InternalService(),
        ),
        namespace="kernel",
        visibility=DependencyVisibility.PRIVATE,
    )

    with pytest.raises(
        DependencyVisibilityError,
    ):
        manager.resolve(
            InternalService,
            namespace="kernel",
        )
