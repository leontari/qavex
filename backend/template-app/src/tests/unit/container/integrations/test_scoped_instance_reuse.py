import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import DependencyScope
from tests.plugins.container import namespace


@pytest.mark.asyncio
async def test_scoped_instance_reuse(
    container: Container,
    namespace: Namespace,
) -> None:
    class Service:
        pass

    class Provider:
        async def provide(self, resolver):
            return Service()

    container.register(
        contract=Service,
        provider=Provider(),
        scope=DependencyScope.SCOPED,
        namespace=namespace,
    )

    async with container.scope():
        first = await container.resolve(Service, namespace=namespace)
        second = await container.resolve(Service, namespace=namespace)

        assert first is second
