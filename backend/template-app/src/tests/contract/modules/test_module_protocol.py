from __future__ import annotations

from typing import Protocol

from template_app.runtime.modules.context import (
    ModuleContext,
)

from tests.support.factories.modules import (
    build_fake_module,
)


class ModuleProtocol(Protocol):

    def setup(
        self,
        context: ModuleContext,
    ) -> None: ...


def test_module_protocol_compatible() -> None:

    module = build_fake_module()

    assert isinstance(
        module.setup,
        object,
    )
