from __future__ import annotations

from tests.support.fakes.modules import build_fake_module


def test_module_protocol_compatible() -> None:

    module = build_fake_module()

    assert isinstance(module.setup, object)
    assert callable(module.setup)
