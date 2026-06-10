"""Dependency metadata storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.container.exceptions import (
    DependencyAlreadyRegisteredError,
    DependencyNotFoundError,
)

if TYPE_CHECKING:
    from template_app.runtime.container.models.dependency import (
        DependencyDescriptor,
        DependencyID,
    )
    from template_app.runtime.container.models.namespace import Namespace


@dataclass(slots=True)
class DependencyRegistry:
    """
    Metadata storage.

    Registry stores dependency metadata only.

    """

    _descriptors: dict[DependencyID, DependencyDescriptor] = field(
        default_factory=dict,
    )

    def add(self, descriptor: DependencyDescriptor) -> None:
        """
        Store dependency metadata.

        Raises:
            DependencyAlreadyRegisteredError:
                if dependency is registered.

        """
        if descriptor.ident in self._descriptors:
            raise DependencyAlreadyRegisteredError(descriptor.ident)

        self._descriptors[descriptor.ident] = descriptor

    def replace(self, descriptor: DependencyDescriptor) -> None:
        """Replace stored dependency metadata."""
        if descriptor.ident not in self._descriptors:
            raise DependencyNotFoundError(descriptor.ident)

        self._descriptors[descriptor.ident] = descriptor

    def get(self, dependency_id: DependencyID) -> DependencyDescriptor:
        """
        Get stored descriptor metadata by ID.

        Returns:
            DependencyDescriptor.

        Raises:
            DependencyNotFoundError:
                If dependency is not registered.

        """
        try:
            return self._descriptors[dependency_id]

        except KeyError as error:
            raise DependencyNotFoundError(dependency_id) from error

    def remove(self, dependency_id: DependencyID) -> DependencyDescriptor:
        """
        Remove stored dependency metadata by ID.

        Returns:
            removed DependencyDescriptor.

        Raises:
            DependencyNotFoundError:
                If dependency is not registered.

        """
        try:
            return self._descriptors.pop(dependency_id)

        except KeyError as error:
            raise DependencyNotFoundError(dependency_id) from error

    def contains(self, dependency_id: DependencyID) -> bool:
        """
        Whether dependency metadata is in storage.

        Returns:
            True if dependency descriptor is registered.

        """
        return dependency_id in self._descriptors

    @property
    def descriptors(self) -> tuple[DependencyDescriptor, ...]:
        """
        Return immutable view of registered descriptors.

        Helper for:
            - GraphBuilder;
            - Diagnostics;
            - Exporters;
            - PluginLoader.
        """
        return tuple(self._descriptors.values())

    @property
    def dependency_ids(self) -> tuple[DependencyID, ...]:
        """
        Return immutable list of registered keys.

        Helper for:
            - Diagnostics;
            - Graph;
            - Validation.

        """
        return tuple(self._descriptors.keys())

    @property
    def namespaces(self) -> frozenset[Namespace]:
        """
        Return unique namespace models stored in registry.

        Helper for:
            - PluginDiagnostics;
            - VisibilityChecks;
            - GraphExport.

        """
        return frozenset(
            descriptor.ident.namespace
            for descriptor in self._descriptors.values()
        )

    def items(self) -> tuple[tuple[DependencyID, DependencyDescriptor], ...]:
        """
        Return immutable snapshot of registered dependencies.

        Helper for:
            - GraphBuilder.

        Returns:
            immutable snapshot of stored dependencies.

        """
        return tuple(self._descriptors.items())

    @property
    def size(self) -> int:
        """
        Return number of registered dependencies.

        Helper for:
            - testing.
        """
        return len(self._descriptors)

    @property
    def is_empty(self) -> bool:
        """
        Whether dependency storage is empty.

        Helper for:
            - testing.

        Returns:
            True if storage is empty.

        """
        return len(self._descriptors) == 0

    def clear(self) -> None:
        """
        Clear storage.

        Helper for:
            - testing.
        """
        self._descriptors.clear()
