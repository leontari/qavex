from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.transports.cli.transport import CLITransport
from template_app.runtime.transports.grpc.transport import GRPCTransport
from template_app.runtime.transports.http.transport import FastAPITransport
from template_app.runtime.transports.kafka.transport import KafkaTransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel
    from template_app.runtime.transports.contracts import Transport


class TransportFactory:
    """
    Creates transport instances without side effects.

    Note:
        NO INSTALL HERE.

    """

    @staticmethod
    def create_http(kernel: RuntimeKernel, app) -> Transport:
        return FastAPITransport(app=app)

    @staticmethod
    def create_cli(kernel: RuntimeKernel) -> Transport:
        return CLITransport(kernel)

    @staticmethod
    def create_grpc(kernel: RuntimeKernel, server) -> Transport:
        return GRPCTransport(server=server, kernel=kernel)

    @staticmethod
    def create_kafka(kernel: RuntimeKernel, consumer) -> Transport:
        return KafkaTransport(consumer=consumer, kernel=kernel)
