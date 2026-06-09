from __future__ import annotations

import pytest

from template_app.runtime.container.exceptions import (
    DependencyAlreadyRegisteredError,
)
from template_app.runtime.container.runtime.registry import (
    DependencyRegistry,
)
from template_app.runtime.container.types import (
    DependencyVisibility,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Service:
    pass


def test_register_dependency() -> None:
    registry = DependencyRegistry()

    registry.register(
        namespace="kernel",
        contract=Service,
        provider=SingletonProvider(
            lambda _: Service(),
        ),
        visibility=DependencyVisibility.PUBLIC,
    )

    assert registry.contains(
        "kernel",
        Service,
    )


def test_duplicate_registration_raises() -> None:
    registry = DependencyRegistry()

    registry.register(
        namespace="kernel",
        contract=Service,
        provider=SingletonProvider(
            lambda _: Service(),
        ),
        visibility=DependencyVisibility.PUBLIC,
    )

    with pytest.raises(
        DependencyAlreadyRegisteredError,
    ):
        registry.register(
            namespace="kernel",
            contract=Service,
            provider=SingletonProvider(
                lambda _: Service(),
            ),
            visibility=DependencyVisibility.PUBLIC,
        )


def test_overwrite_registration() -> None:
    registry = DependencyRegistry()

    registry.register(
        namespace="kernel",
        contract=Service,
        provider=SingletonProvider(
            lambda _: Service(),
        ),
        visibility=DependencyVisibility.PUBLIC,
    )

    registry.register(
        namespace="kernel",
        contract=Service,
        provider=SingletonProvider(
            lambda _: Service(),
        ),
        visibility=DependencyVisibility.PUBLIC,
        overwrite=True,
    )

    assert registry.contains(
        "kernel",
        Service,
    )
