from __future__ import annotations

import pytest

from template_app.bootstrap.dispatching.queries.dispatcher import (
    QueryDispatcher,
)
from template_app.bootstrap.dispatching.queries.models import (
    Query,
)
from template_app.bootstrap.dispatching.registry import (
    MessageHandlerRegistry,
)


class GetUserQuery(Query):
    pass


@pytest.mark.asyncio
async def test_query_dispatcher_returns_result() -> None:

    registry = MessageHandlerRegistry()

    async def handler(_: Query) -> str:
        return "user"

    registry.register_query(
        GetUserQuery,
        handler,
    )

    dispatcher = QueryDispatcher(
        registry=registry,
    )

    result = await dispatcher.ask(
        GetUserQuery(),
    )

    assert result == "user"
