from __future__ import annotations

import pytest

from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)

from template_app.runtime.transports.grpc.transport import (
    GRPCTransport,
)

from template_app.runtime.transports.kafka.transport import (
    KafkaTransport,
)

from template_app.runtime.transports.cli.transport import (
    CLITransport,
)


@pytest.fixture
def http_transport() -> FastAPITransport:
    return FastAPITransport()


@pytest.fixture
def grpc_transport() -> GRPCTransport:
    return GRPCTransport()


@pytest.fixture
def kafka_transport() -> KafkaTransport:
    return KafkaTransport()


@pytest.fixture
def cli_transport() -> CLITransport:
    return CLITransport()
