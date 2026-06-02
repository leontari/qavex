"""Transport specific assertions."""

from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.contracts import Transport


def assert_transport_installed(
    kernel: RuntimeKernel,
    transport_type: Transport
) -> None:
    """
    Assert runtime transport installed.
    """
    assert kernel.transport_manager.get(transport_type) is not None
