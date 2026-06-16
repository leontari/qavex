import asyncio

import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import DependencyScope


@pytest.mark.asyncio
async def test_concurrent_scoped_resolution(
    container: Container,
    namespace: Namespace,
) -> None:
    calls = 0

    class Service:
        pass

    class Provider:
        async def provide(self, resolver):
            nonlocal calls

            calls += 1

            await asyncio.sleep(0.05)

            return Service()

    container.register(
        contract=Service,
        provider=Provider(),
        scope=DependencyScope.SCOPED,
        namespace=namespace,
    )

    async with container.scope():

        first, second, third = await asyncio.gather(
            container.resolve(Service, namespace=namespace),
            container.resolve(Service, namespace=namespace),
            container.resolve(Service, namespace=namespace),
        )

        assert first is second
        assert second is third

    assert calls == 1
