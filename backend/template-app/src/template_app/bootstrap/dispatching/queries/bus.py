from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.queries.models import (
        Query,
    )
    from template_app.bootstrap.dispatching.registry import (
        MessageHandlerRegistry,
    )


@dataclass(slots=True)
class InMemoryQueryBus:
    registry: MessageHandlerRegistry

    async def ask(self, query: Query) -> Any:

        handler = self.registry._queries[type(query)]

        return await handler(query)
