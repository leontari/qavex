from __future__ import annotations

from template_app.runtime.container.providers import (
    AsyncProvider,
    FactoryProvider,
    SingletonProvider,
)


class Service:
    pass


def test_singleton_provider_contract() -> None:
    provider = SingletonProvider(
        lambda _: Service(),
    )

    assert hasattr(provider, "scope")
    assert hasattr(provider, "provide")


def test_factory_provider_contract() -> None:
    provider = FactoryProvider(
        lambda _: Service(),
    )

    assert hasattr(provider, "scope")
    assert hasattr(provider, "provide")


def test_async_provider_contract() -> None:
    async def factory(_: object) -> Service:
        return Service()

    provider = AsyncProvider(factory)

    assert hasattr(provider, "scope")
    assert hasattr(provider, "provide")
