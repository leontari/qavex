"""Module registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.modules.manifests import ModuleManifest


@dataclass(slots=True)
class ModuleRegistry:
    """
    Runtime module registry.

    Responsibilities:
        - module ownership
        - module lookup
        - module enumeration

    """

    _modules: dict[str, ModuleManifest] = field(
        default_factory=dict,
    )

    def register(self, manifest: ModuleManifest) -> None:
        """
        Register module manifest.

        Args:
            manifest:
                Module manifest.

        Raises:
            RuntimeError:
                If module already registered.

        """
        if manifest.name in self._modules:
            msg = f"Module already registered: {manifest.name}"
            raise RuntimeError(msg)

        self._modules[manifest.name] = manifest

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        """
        Return immutable module snapshot.

        Returns:
            Registered modules snapshot.

        """
        return tuple(self._modules.values())
