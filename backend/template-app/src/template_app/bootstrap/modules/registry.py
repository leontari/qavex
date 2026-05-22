"""Runtime graph of the loaded modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.modules.manifests import ModuleManifest


@dataclass(slots=True)
class ModuleRegistry:
    """Application module registry."""

    _modules: dict[str, ModuleManifest] = field(
        default_factory=dict,
    )

    def register(self, manifest: ModuleManifest) -> None:
        self._modules[manifest.name] = manifest

    def get(self, name: str) -> ModuleManifest:
        return self._modules[name]

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        return tuple(self._modules.values())
