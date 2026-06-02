from __future__ import annotations

from template_app.runtime.transports.http.transport import FastAPITransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_http_transport_registered() -> None:
    kernel = KernelTestHarness().kernel

    transport = kernel.transport_manager.get(FastAPITransport)

    assert transport is not None


def test_http_transport_exposed_via_kernel() -> None:
    kernel = KernelTestHarness().kernel

    assert len(kernel.transports) > 0
