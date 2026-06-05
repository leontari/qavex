"""Runtime dependency namespaces."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DependencyNamespace(StrEnum):
    """Built-in runtime namespaces."""

    KERNEL = "kernel"
    INFRASTRUCTURE = "infrastructure"
    TRANSPORT = "transport"
    MODULE = "module"
    PLUGIN = "plugin"
    GUI = "gui"
    TESTING = "testing"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class Namespace:
    """Logical dependency namespace."""

    name: str

    def __str__(self) -> str:
        return self.name
