from __future__ import annotations

import pytest

from template_app.bootstrap.messaging.buses import QueryBus
from template_app.bootstrap.messaging.queries import Query
from template_app.bootstrap.messaging.registry import (
    MessageHandlerRegistry,
)


class GetUser(Query):
    pass


class GetUserHandler:

    async def handle(self, query: GetUser) -> dict[str, str]:
        return {"name": "admin"}


@pytest.mark.asyncio
async def test_query_bus_executes_query() -> None:
    registry = MessageHandlerRegistry()

    registry.register_query_handler(
        GetUser,
        GetUserHandler(),
    )

    bus = QueryBus(registry=registry)

    result = await bus.execute(GetUser())

    assert result["name"] == "admin"
