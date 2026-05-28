from __future__ import annotations

import pytest

from template_app.runtime.messaging.contracts.queries import (
    Query,
)
from template_app.runtime.messaging.buses.query_bus import (
    RuntimeQueryBus,
)
from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)


class GetUserQuery(Query):
    pass


@pytest.mark.asyncio
async def test_runtime_query_bus_returns_result() -> None:

    registry = RuntimeHandlerRegistry()

    async def handler(_: Query) -> str:
        return "user"

    registry.register_query_handler(
        GetUserQuery,
        handler,
    )

    bus = RuntimeQueryBus(
        registry=registry,
    )

    result = await bus.ask(
        GetUserQuery(),
    )

    assert result == "user"
