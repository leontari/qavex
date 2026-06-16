import pytest

from template_app.runtime.container.models.scope import DependencyScope


@pytest.mark.asyncio
async def test_scoped_instance_isolation(container: Container) -> None:
    class Service:
        pass

    class Provider:
        async def provide(self, resolver):
            return Service()

    container.register(
        contract=Service,
        provider=Provider(),
        scope=DependencyScope.SCOPED,
    )

    async with container.scope():
        first = await container.resolve(Service)

    async with container.scope():
        second = await container.resolve(Service)

    assert first is not second
