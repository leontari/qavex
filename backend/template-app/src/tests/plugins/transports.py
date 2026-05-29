from __future__ import annotations

from collections.abc import Iterator

import pytest

from template_app.runtime.transports.manager import TransportManager
from tests.support.fakes.transports import FakeTransport
from tests.support.testing.transport_builder import TransportBuilder

########################
# transport infrastructure
########################

@pytest.fixture
def transport_manager(kernel) -> TransportManager:
    """
    Return runtime transport manager.
    """
    return kernel.transport_manager

########################
# fake transports
########################

@pytest.fixture
def fake_transport() -> FakeTransport:
    """
    Return generic fake transport.
    """
    return TransportBuilder.fake()


@pytest.fixture
def http_fake_transport() -> FakeTransport:
    """
    Return fake HTTP transport.
    """
    return TransportBuilder.fake(name="http")


@pytest.fixture
def grpc_fake_transport() -> FakeTransport:
    """
    Return fake gRPC transport.
    """
    return TransportBuilder.fake(
        name="grpc",
    )


@pytest.fixture
def kafka_fake_transport() -> FakeTransport:
    """
    Return fake Kafka transport.
    """
    return TransportBuilder.fake(
        name="kafka",
    )


@pytest.fixture
def cli_fake_transport() -> FakeTransport:
    """
    Return fake CLI transport.
    """
    return TransportBuilder.fake(
        name="cli",
    )

########################
# installed transports
########################

@pytest.fixture
def installed_transport(
    transport_manager: TransportManager,
    fake_transport: FakeTransport,
) -> Iterator[FakeTransport]:
    """
    Install fake transport into runtime.
    """
    transport_manager.install(
        fake_transport,
    )

    yield fake_transport

########################
# parametrized transports
########################

@pytest.fixture(params=["http", "grpc", "kafka", "cli"])
def transport_kind(request) -> str:
    """
    Parametrized transport kind.
    """
    return request.param


@pytest.fixture
def parametrized_transport(transport_kind: str) -> FakeTransport:
    """
    Return parametrized fake transport.
    """
    return TransportBuilder.fake(
        name=transport_kind,
    )


@pytest.fixture
def installed_parametrized_transport(
    transport_manager: TransportManager,
    parametrized_transport: FakeTransport,
) -> Iterator[FakeTransport]:
    """
    Install parametrized transport.
    """
    transport_manager.install(
        parametrized_transport,
    )

    yield parametrized_transport
