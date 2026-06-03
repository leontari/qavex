from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder

from tests.support.fakes.transports import FakeTransport


def test_freeze_installs_transports() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()
    transport = FakeTransport()

    builder.install_transport(composition, transport)
    builder.freeze(composition)

    assert transport in composition.kernel.transports
