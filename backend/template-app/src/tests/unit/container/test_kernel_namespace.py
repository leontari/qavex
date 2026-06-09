from __future__ import annotations

from template_app.runtime.container.runtime.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class KernelConfig:
    pass


def test_kernel_namespace_registration() -> None:
    manager = DependencyManager()

    manager.register(
        KernelConfig,
        SingletonProvider(
            lambda _: KernelConfig(),
        ),
        namespace="kernel",
    )

    instance = manager.resolve(
        KernelConfig,
        namespace="kernel",
    )

    assert isinstance(
        instance,
        KernelConfig,
    )


def test_kernel_namespace_contains_contract() -> None:
    manager = DependencyManager()

    manager.register(
        KernelConfig,
        SingletonProvider(
            lambda _: KernelConfig(),
        ),
        namespace="kernel",
    )

    assert manager.contains(
        KernelConfig,
        namespace="kernel",
    )
