from __future__ import annotations

import pytest

from template_app.runtime.application.builder import ApplicationBuilder
from tests.support.fakes.transports import FakeTransport


def test_freeze_installs_transports() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()
    transport = FakeTransport()

    builder.install_transport(
        composition,
        transport,
    )

    builder.freeze(composition)

    assert transport in composition.kernel.transports


def test_freeze_locks_kernel() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    builder.freeze(composition)

    assert composition.kernel.is_frozen is True


def test_transport_installation_after_freeze_rejected() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    builder.freeze(composition)

    with pytest.raises(RuntimeError):
        composition.kernel.install_transport(FakeTransport())


# def test_builder_freezes_kernel(kernel: RuntimeKernel) -> None:
#     builder = ApplicationBuilder()
#     app = builder.create()
#
#     assert app.kernel.metadata.freeze.frozen is True
#     assert kernel.is_frozen is True
