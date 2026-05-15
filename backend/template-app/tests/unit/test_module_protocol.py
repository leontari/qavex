from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.container import Container
from template_app.bootstrap.protocols import ModuleProtocol


class FakeModule:
    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        app.state.module_loaded = True



def test_module_protocol_compatible() -> None:
    module: ModuleProtocol = FakeModule()

    app = FastAPI()
    container = Container()

    module.setup(app, container)

    assert app.state.module_loaded is True
