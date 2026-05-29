"""Production transport factory for test purposes."""
from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.kernel.kernel import (
    RuntimeKernel,
)
from template_app.runtime.transports.cli.transport import (
    CLITransport,
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


def build_http_transport(
    app: FastAPI,
) -> FastAPITransport:
    """
    Build production HTTP transport.
    """
    return FastAPITransport(
        app=app,
    )


def build_grpc_transport(
    server,
    kernel: RuntimeKernel,
) -> GRPCTransport:
    """
    Build production gRPC transport.
    """
    return GRPCTransport(
        server=server,
        kernel=kernel,
    )


def build_kafka_transport(
    consumer,
    kernel: RuntimeKernel,
) -> KafkaTransport:
    """
    Build production Kafka transport.
    """
    return KafkaTransport(
        consumer=consumer,
        kernel=kernel,
    )


def build_cli_transport(
    kernel: RuntimeKernel,
) -> CLITransport:
    """
    Build production CLI transport.
    """
    return CLITransport(
        kernel=kernel,
    )
