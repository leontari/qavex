from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.bootstrap.messaging.contracts.queries import Query
    from template_app.bootstrap.messaging.runtime.registry import (
        RuntimeHandlerRegistry,
    )


@dataclass(slots=True)
class RuntimeQueryBus:
    """Runtime query bus."""

    registry: RuntimeHandlerRegistry

    async def ask(self, query: Query) -> Any:

        handler = self.registry.get_query_handler(type(query))

        return await handler(query)
