from __future__ import annotations

from template_app.runtime.container.manager import (
    DependencyManager,
)
from template_app.runtime.container.providers import (
    SingletonProvider,
)


class ServiceV1:
    version = "v1"


class ServiceV2:
    version = "v2"


class Service:
    pass


def test_overwrite_dependency_registration() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: ServiceV1(),
        ),
        namespace="kernel",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: ServiceV2(),
        ),
        namespace="kernel",
        overwrite=True,
    )

    instance = manager.resolve(
        Service,
        namespace="kernel",
    )

    assert isinstance(
        instance,
        ServiceV2,
    )


def test_overwrite_replaces_provider() -> None:
    manager = DependencyManager()

    provider_v1 = SingletonProvider(
        lambda _: ServiceV1(),
    )

    provider_v2 = SingletonProvider(
        lambda _: ServiceV2(),
    )

    manager.register(
        Service,
        provider_v1,
        namespace="kernel",
    )

    manager.register(
        Service,
        provider_v2,
        namespace="kernel",
        overwrite=True,
    )

    descriptor = manager.registry.get(
        "kernel",
        Service,
    )

    assert descriptor.provider is provider_v2


def test_overwrite_keeps_namespace_isolation() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(
            lambda _: ServiceV1(),
        ),
        namespace="kernel",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: ServiceV2(),
        ),
        namespace="plugin.billing",
    )

    manager.register(
        Service,
        SingletonProvider(
            lambda _: ServiceV2(),
        ),
        namespace="kernel",
        overwrite=True,
    )

    kernel_instance = manager.resolve(
        Service,
        namespace="kernel",
    )

    plugin_instance = manager.resolve(
        Service,
        namespace="plugin.billing",
    )

    assert isinstance(
        kernel_instance,
        ServiceV2,
    )

    assert isinstance(
        plugin_instance,
        ServiceV2,
    )

    assert kernel_instance is not plugin_instance
