from __future__ import annotations


def assert_transport_installed(
    kernel,
    transport_type,
) -> None:
    """
    Assert runtime transport installed.
    """
    assert (
        kernel.transport_manager.get(
            transport_type,
        )
        is not None
    )
