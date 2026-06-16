"""Singleton instances storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import Future
    from collections.abc import Iterator, Mapping

    from template_app.runtime.container.models.dependency import DependencyID


@dataclass(slots=True)
class SingletonCache:
    """
    Singleton instance cache.

    Source of truth for singleton instances.

    Stores:
        - initialized singleton instances
        - singleton creation futures

    Notes:
        Synchronization and race-condition prevention are
        handled by DependencyManager.

        SingletonCache is a storage component only.

    """

    _instances: dict[DependencyID, object] = field(
        default_factory=dict,
    )

    _futures: dict[DependencyID, Future[object]] = field(
        default_factory=dict,
    )

    def contains(self, dependency_id: DependencyID) -> bool:
        """
        Whether singleton instance exists.

        Returns:
            True if singleton instance is cached.

        """
        return dependency_id in self._instances

    def contains_future(self, dependency_id: DependencyID) -> bool:
        """
        Whether initialization future exists.

        Returns:
            True if initialization future is registered.

        """
        return dependency_id in self._futures

    def get(self, dependency_id: DependencyID) -> object:
        """
        Get singleton instance.

        Returns:
            Cached singleton instance.

        Raises: KeyError If instance is not cached.

        """
        return self._instances[dependency_id]

    def get_future(self, dependency_id: DependencyID) -> Future[object] | None:
        """
        Get initialization future.

        Returns:
            Registered initialization future or None

        """
        return self._futures.get(dependency_id)

    def set(self, dependency_id: DependencyID, instance: object) -> None:
        """Store singleton instance."""
        self._instances[dependency_id] = instance

    def set_future(
        self, dependency_id: DependencyID, future: Future[object]
    ) -> None:
        """Store initialization future."""
        self._futures[dependency_id] = future

    def remove(self, dependency_id: DependencyID) -> None:
        """
        Remove singleton instance.

        Missing instances are ignored.
        """
        self._instances.pop(dependency_id, None)

    def remove_future(self, dependency_id: DependencyID) -> None:
        """
        Remove initialization future.

        Missing futures are ignored.
        """
        self._futures.pop(dependency_id, None)

    def iter_instances(self) -> Iterator[tuple[DependencyID, object]]:
        """
        Iterate over cached singleton instances.

        Returns:
            Iterator over cached instances.

        """
        return iter(self._instances.items())

    def iter_futures(self) -> Iterator[Future[object]]:
        """
        Iterate over registered initialization futures.

        Returns:
            Iterator over active initialization futures.

        """
        return iter(self._futures.values())

    def clear(self) -> None:
        """
        Remove all cached state.

        Clears:
            - singleton instances
            - initialization futures
        """
        self._instances.clear()
        self._futures.clear()

    #############
    # Diagnostics
    #############

    @property
    def instances(self) -> Mapping[DependencyID, object]:
        """
        Immutable singleton instances view.

        Returns:
            Read-only mapping of cached singleton instances.

        """
        return MappingProxyType(self._instances)

    @property
    def futures(self) -> MappingProxyType[DependencyID, Future[object]]:
        """
        Read-only initialization futures view.

        Returns:
            Immutable snapshot of initialization futures.

        """
        return MappingProxyType(self._futures)

    @property
    def count(self) -> int:
        """
        Cached singleton instances count.

        Returns:
            Number of cached singleton instances.

        """
        return len(self._instances)

    @property
    def future_count(self) -> int:
        """
        Active initialization future count.

        Returns:
            Number of registered initialization futures.

        """
        return len(self._futures)
