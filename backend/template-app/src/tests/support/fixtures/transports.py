from __future__ import annotations

import pytest

from template_app.runtime.transports.manager import (
    TransportManager,
)
from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)
from template_app.runtime.transports.kafka.transport import (
    KafkaTransport,
)
from template_app.runtime.transports.grpc.transport import (
    GRPCTransport,
)
from template_app.runtime.transports.cli.transport import (
    CLITransport,
)


@pytest.fixture
def transport_manager(runtime) -> TransportManager:
    """
    Return runtime transport manager.
    """
    return runtime.transports.manager


@pytest.fixture
def http_transport(transport_manager):
    transport = FastAPITransport()

    transport_manager.install(transport)

    return transport


@pytest.fixture
def kafka_transport(transport_manager):
    transport = KafkaTransport()

    transport_manager.install(transport)

    return transport


@pytest.fixture
def grpc_transport(transport_manager):
    transport = GRPCTransport()

    transport_manager.install(transport)

    return transport


@pytest.fixture
def cli_transport(transport_manager):
    transport = CLITransport()

    transport_manager.install(transport)

    return transport
