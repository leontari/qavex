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

    _descriptors: dict[DependencyID:DependencyDescriptor] = field(
        default_factory=dict,
    )

    def add(self, descriptor: DependencyDescriptor) -> None:
        """
        Store dependency metadata.

        Raises:
            DependencyAlreadyRegisteredError

        """
        if self._descriptors[descriptor.ident] in self._descriptors:
            raise DependencyAlreadyRegisteredError(descriptor)

        self._descriptors[descriptor.ident] = descriptor

    def replace(self, descriptor: DependencyDescriptor) -> None:
        """Replace stored dependency metadata."""
        self._descriptors[descriptor.ident] = descriptor

    def get(self, dependency_id: DependencyID) -> DependencyDescriptor:
        """
        Get stored descriptor metadata by ID.

        To be use in runtime container.

        Returns:
            DependencyDescriptor

        Raises:
            DependencyNotFoundError

        """
        try:
            return self._descriptors[dependency_id]

        except KeyError as error:
            raise DependencyNotFoundError(dependency_id) from error

    def remove(self, dependency_id: DependencyID) -> DependencyDescriptor:
        """
        Remove stored dependency metadata by ID.

        Returns:
            removed DependencyDescriptor

        """
        return self._descriptors.pop(dependency_id)

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
        Return immutable metadata view.

        Helper for:
            - GraphBuilder
            - Diagnostics
            - Exporters
            - PluginLoader
        """
        return tuple(self._descriptors.values())

    @property
    def dependency_ids(self) -> tuple[DependencyID, ...]:
        """
        Return immutable list of registered keys.

        Helper for:
            - Diagnostics
            - Graph
            - Validation

        """
        return tuple(self._descriptors.keys())

    @property
    def namespaces(self) -> frozenset[Namespace]:
        """
        Return unique namespace models stored in registry.

        Helper for:
            - PluginDiagnostics
            - VisibilityChecks
            - GraphExport

        """
        return frozenset(
            descriptor.ident.namespace
            for descriptor in self._descriptors.values()
        )

    def clear(self) -> None:
        """
        Clear storage.

        Helper for:
            - testing
        """
        self._descriptors.clear()
