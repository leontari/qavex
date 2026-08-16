"""DI provider factory."""

from __future__ import annotations

from dataclasses import dataclass
from inspect import isawaitable
from typing import TYPE_CHECKING, Generic

from .type_vars import T

if TYPE_CHECKING:
    from .contracts import DependencyResolver
    from .type_aliases import Factory


@dataclass(slots=True, frozen=True)
class FactoryProvider(Generic[T]):
    """Universal dependency provider factory."""

    factory: Factory[T]

    async def provide(self, resolver: DependencyResolver) -> T:
        """
        Provide dependency object.

        Returns:
            Resolved dependency object

        """
        result = self.factory(resolver)

        if isawaitable(result):
            result = await result

        return result
