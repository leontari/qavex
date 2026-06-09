from __future__ import annotations

import pytest

from template_app.runtime.container.exceptions import (
    DependencyNotFoundError,
)
from template_app.runtime.container.runtime.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class Service:
    pass


def test_namespaces_are_isolated() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="kernel",
    )

    with pytest.raises(
        DependencyNotFoundError,
    ):
        manager.resolve(
            Service,
            namespace="plugin.billing",
        )


def test_same_contract_can_exist_in_multiple_namespaces() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="kernel",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: Service(),
        ),
        namespace="plugin.billing",
    )

    kernel_instance = manager.resolve(
        Service,
        namespace="kernel",
    )

    plugin_instance = manager.resolve(
        Service,
        namespace="plugin.billing",
    )

    assert kernel_instance is not plugin_instance
