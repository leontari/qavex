from __future__ import annotations

from collections.abc import Iterator

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.contracts import Transport
from tests.support.fakes.transports import FakeTransport


def test_transport_runtime_exposes_immutable_snapshot(kernel) -> None:
    """
    Kernel should expose immutable transport snapshot.
    """
    transports = kernel.transports

    assert isinstance(transports, tuple)


def test_transport_manager_returns_transport_protocol(
    installed_transport: FakeTransport,
    kernel: RuntimeKernel,
) -> None:
    """
    Installed transport should satisfy contract.
    """
    resolved = kernel.transport_manager.get(
        type(installed_transport),
    )

    assert resolved is not None
    assert isinstance(resolved, Transport)
