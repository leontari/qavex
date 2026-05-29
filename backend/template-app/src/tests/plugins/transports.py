from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from template_app.runtime.transports.cli.transport import (
    CLITransport,
)
from template_app.runtime.transports.contracts import (
    Transport,
)
from template_app.runtime.transports.grpc.transport import (
    GRPCTransport,
)
from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)
from template_app.runtime.transports.kafka.transport import (
    KafkaTransport,
)
from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)

TransportFactory = Callable[..., Transport]


@pytest.fixture
def transport_factory() -> TransportFactory:
    """
    Generic runtime transport factory.

    Returns:
        Transport factory callable.
    """

    registry: dict[str, type[Transport]] = {
        "http": FastAPITransport,
        "grpc": GRPCTransport,
        "kafka": KafkaTransport,
        "cli": CLITransport,
    }

    def factory(
        transport_type: str,
        **kwargs: Any,
    ) -> Transport:
        """
        Build runtime transport.

        Args:
            transport_type:
                Runtime transport type.

        Returns:
            Runtime transport.

        Raises:
            KeyError:
                Unknown transport type.
        """
        transport_cls = registry[
            transport_type
        ]

        return transport_cls(
            **kwargs,
        )

    return factory


@pytest.fixture
def installed_transport(
    kernel_harness: KernelTestHarness,
):
    """
    Install runtime transport dynamically.

    Returns:
        Installed transport factory.
    """

    def installer(
        transport: Transport,
    ) -> Transport:
        kernel_harness.install_transport(
            transport,
        )

        return transport

    return installer


@pytest.fixture(
    params=[
        "http",
        "grpc",
        "kafka",
        "cli",
    ],
)
def transport_type(
    request: pytest.FixtureRequest,
) -> str:
    """
    Parametrized runtime transport type.
    """
    return str(request.param)


@pytest.fixture
def transport(
    transport_factory: TransportFactory,
    installed_transport,
    transport_type: str,
) -> Transport:
    """
    Parametrized installed runtime transport.

    Returns:
        Installed runtime transport.
    """
    runtime_transport = transport_factory(
        transport_type,
    )

    return installed_transport(
        runtime_transport,
    )
