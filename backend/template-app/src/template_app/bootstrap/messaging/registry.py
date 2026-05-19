from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.bootstrap.messaging.exceptions import (
    HandlerNotRegisteredError,
)

if TYPE_CHECKING:
    from template_app.bootstrap.messaging.commands import Command
    from template_app.bootstrap.messaging.handlers import (
        CommandHandler,
        QueryHandler,
    )
    from template_app.bootstrap.messaging.queries import Query


@dataclass(slots=True)
class MessageHandlerRegistry:
    """Command/query handler registry."""

    _command_handlers: dict[type[Command], CommandHandler] = field(
        default_factory=dict
    )

    _query_handlers: dict[type[Query], QueryHandler] = field(
        default_factory=dict
    )

    def register_command_handler(
        self,
        command_type: type[Command],
        handler: CommandHandler,
    ) -> None:
        self._command_handlers[command_type] = handler

    def register_query_handler(
        self,
        query_type: type[Query],
        handler: QueryHandler,
    ) -> None:
        self._query_handlers[query_type] = handler

    def get_command_handler(
        self,
        command_type: type[Command],
    ) -> CommandHandler:

        try:
            return self._command_handlers[command_type]

        except KeyError as error:
            msg = f"Command handler not registered: {command_type.__name__}"
            raise HandlerNotRegisteredError(msg) from error

    def get_query_handler(self, query_type: type[Query]) -> QueryHandler:

        try:
            return self._query_handlers[query_type]

        except KeyError as error:
            msg = f"Query handler not registered: {query_type.__name__}"
            raise HandlerNotRegisteredError(msg) from error

    @property
    def command_handlers(self) -> dict[type[Command], CommandHandler]:
        return dict(self._command_handlers)

    @property
    def query_handlers(self) -> dict[type[Query], QueryHandler]:
        return dict(self._query_handlers)
