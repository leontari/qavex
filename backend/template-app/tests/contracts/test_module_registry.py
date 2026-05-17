from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.modules import MODULES
from template_app.bootstrap.container import Container
from template_app.bootstrap.contracts import ModuleProtocol
from template_app.bootstrap.registry import ModuleRegistry


def test_modules_registered() -> None:
    assert len(MODULES) >0



class FakeModule:
    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        app.state.loaded = True



def test_module_registry_registers_modules() -> None:
    registry = ModuleRegistry()

    module = FakeModule()

    registry.register(module)

    assert registry.modules == (module,)



def test_module_registry_extend() -> None:
    registry = ModuleRegistry()

    modules: list[ModuleProtocol] = [
        FakeModule(),
        FakeModule(),
    ]

    registry.extend(modules)

    assert len(registry.modules) == 2
