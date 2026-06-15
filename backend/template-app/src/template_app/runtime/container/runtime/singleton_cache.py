"""Singleton instances storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import Future

    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True)
class SingletonCache:
    """
    Singleton instances storage.

    Source of truth for singleton instances.
    """

    _instances: dict[DependencyID, object] = field(
        default_factory=dict,
    )

    _futures: dict[DependencyID, Future[object]] = field(
        default_factory=dict,
    )

    def contains(self, dependency_id: DependencyID) -> bool:
        return dependency_id in self._instances

    def get(self, dependency_id: DependencyID) -> object:
        return self._instances[dependency_id]

    def set(self, dependency_id: DependencyID, instance: object) -> None:
        self._instances[dependency_id] = instance

    def get_future(self, dependency_id: DependencyID) -> Future[object] | None:
        return self._futures.get(dependency_id)

    def set_future(
        self, dependency_id: DependencyID, future: Future[object]
    ) -> None:
        self._futures[dependency_id] = future

    def remove_future(self, dependency_id: DependencyID) -> None:
        self._futures.pop(dependency_id, None)

    def clear(self) -> None:
        self._instances.clear()
        self._futures.clear()
