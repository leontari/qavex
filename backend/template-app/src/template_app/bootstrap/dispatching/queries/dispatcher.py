from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from template_app.bootstrap.dispatching.queries.models import (
        Query,
    )
    from template_app.bootstrap.dispatching.registry import (
        MessageHandlerRegistry,
    )


@dataclass(slots=True)
class QueryDispatcher:
    """Application query dispatcher."""

    registry: MessageHandlerRegistry

    async def ask(self, query: Query) -> Any:

        handler = self.registry.get_query_handler(type(query))

        return await handler(query)
