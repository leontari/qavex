from __future__ import annotations

from template_app.runtime.transports.contracts import (
    Transport,
)


def test_transport_runtime_exposes_immutable_snapshot(
    kernel,
) -> None:
    """
    Kernel should expose immutable transport snapshot.
    """
    transports = kernel.transports

    assert isinstance(
        transports,
        tuple,
    )


def test_transport_manager_returns_transport_protocol(
    transport,
    kernel_harness,
) -> None:
    """
    Installed transport should satisfy contract.
    """
    resolved = kernel_harness.get_transport(
        type(transport),
    )

    assert isinstance(
        resolved,
        Transport,
    )
