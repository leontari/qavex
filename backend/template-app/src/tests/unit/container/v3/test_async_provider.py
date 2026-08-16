import pytest

from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace
from runtime.container.providers import AsyncProvider


class Client:
    pass


async def create_client(_) -> Client:
    return Client()


@pytest.mark.asyncio
async def test_async_provider() -> None:
    manager = DependencyManager()

    manager.register(
        Client,
        AsyncProvider(create_client),
        namespace=Namespace("kernel"),
    )

    client = await manager.resolve_async(Client)

    assert isinstance(client, Client)
