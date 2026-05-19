from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.queries.models import Query


class QueryHandler(Protocol):
    """Query handler contract."""

    async def handle(self, query: Query) -> Any:
        """Handle query."""
