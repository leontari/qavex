from __future__ import annotations

from typing import Any, Protocol

from template_app.bootstrap.messaging.contracts.queries import Query


class RPCQueryGateway(Protocol):
    async def ask(self, query: Query) -> Any: ...
