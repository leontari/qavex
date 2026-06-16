"""Runtime scope state."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

from template_app.runtime.container.models.scope import ScopeState

if TYPE_CHECKING:
    from asyncio import Future
    from collections.abc import Iterator

    from template_app.runtime.container.models.dependency import DependencyID
    from template_app.runtime.container.models.scope import ScopeID


@dataclass(slots=True)
class ScopeContext:
    """
    Runtime scope state.

    Source of truth for scoped instances.

    Owns:
        - scoped instances
        - scoped initialization futures

    ScopeContext exists only while scope is alive.
    """

    id: ScopeID
    state: ScopeState = ScopeState.ACTIVE
    owner_id: str | None = None
    parent_scope: ScopeID | None = None

    _instances: dict[DependencyID, object] = field(default_factory=dict)
    _futures: dict[DependencyID, Future[object]] = field(default_factory=dict)

    def contains(self, dependency_id: DependencyID) -> bool:
        """
        Whether scoped instance exists.

        Returns:
            True if instance is cached.

        """
        return dependency_id in self._instances

    def contains_future(self, dependency_id: DependencyID) -> bool:
        """
        Whether initialization future exists.

        Returns:
            True if initialization future exists.

        """
        return dependency_id in self._futures

    def get(self, dependency_id: DependencyID) -> object:
        """
        Get cached instance.

        Returns:
            Cached instance.

        Raises: KeyError if instance is not cached.

        """
        return self._instances[dependency_id]

    def get_future(self, dependency_id: DependencyID) -> Future[object] | None:
        """
        Get initialization future.

        Returns:
            Registered future or None.

        """
        return self._futures.get(dependency_id)

    def set(self, dependency_id: DependencyID, instance: object) -> None:
        """Store scoped instance."""
        self._instances[dependency_id] = instance

    def set_future(
        self, dependency_id: DependencyID, future: Future[object]
    ) -> None:
        """Store initialization future."""
        self._futures[dependency_id] = future

    def remove(self, dependency_id: DependencyID) -> None:
        """
        Remove cached instance.

        Missing entries are ignored.

        """
        self._instances.pop(dependency_id, None)

    def remove_future(self, dependency_id: DependencyID) -> None:
        """
        Remove initialization future.

        Missing entries are ignored.

        """
        self._futures.pop(dependency_id, None)

    def iter_instances(self) -> Iterator[tuple[DependencyID, object]]:
        """
        Iterate over registered scoped instances.

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
        Remove all scope state.

        Clears:
            - scoped instances
            - initialization futures

        """
        self._instances.clear()
        self._futures.clear()

    #############
    # Diagnostics
    #############

    @property
    def instances(self) -> MappingProxyType[DependencyID, object]:
        """
        Immutable scoped instances view.

        Returns:
            Read-only mapping of scoped instances.

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
        Cached scoped instances count.

        Returns:
            Number of registered scoped instances.

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
