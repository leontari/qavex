"""Plugin contracts."""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import ClassVar

from template_app.runtime.container.namespace import Namespace


@runtime_checkable
class PluginDeclaration(Protocol):
    """
    Declarative plugin contract.

    Used by Kernel autodiscovery
    """

    name: str
    namespace: str
    version: str
    dependencies: tuple[type[Any], ...]
    exports: tuple[type[Any], ...]


@dataclass(slots=True)
class Plugin:
    """Base plugin declaration."""

    name: ClassVar[str]
    namespace: ClassVar[Namespace]

    requires: ClassVar[tuple[str, ...]] = ()
    exports: ClassVar[tuple[type, ...]] = ()


class PluginLoader:
    """Runtime plugin discovery."""

    def discover(
        self,
        package_name: str,
    ) -> list[type[Plugin]]:
        """Discover plugins recursively."""
        package = importlib.import_module(package_name)

        discovered: list[type[Plugin]] = []

        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + ".",
        ):
            module = importlib.import_module(module_name)

            for value in vars(module).values():
                if (
                    isinstance(value, type)
                    and issubclass(value, Plugin)
                    and value is not Plugin
                ):
                    discovered.append(value)

        return discovered
