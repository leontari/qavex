from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel
    from template_app.runtime.transports.cli.transport import CLITransport
    from template_app.runtime.transports.grpc.transport import GRPCTransport
    from template_app.runtime.transports.kafka.transport import KafkaTransport


class TransportFactory:
    """
    Creates transport instances without side effects.

    Transport creation factory:
        ONLY creates transports
        NEVER installs transports.

    """

    @staticmethod
    def create_http(kernel: RuntimeKernel) -> FastAPITransport:
        from template_app.runtime.transports.http.factory import (  # noqa: PLC0415
            create_http_app,
        )

        app = create_http_app(kernel)

        return FastAPITransport(app=app)

    @staticmethod
    def create_cli(kernel: RuntimeKernel) -> CLITransport:
        from template_app.runtime.transports.cli.transport import (  # noqa: PLC0415
            CLITransport,
        )

        return CLITransport(kernel)

    @staticmethod
    def create_grpc(kernel: RuntimeKernel) -> GRPCTransport:
        from template_app.runtime.transports.grpc.transport import (  # noqa: PLC0415
            GRPCTransport,
        )

        return GRPCTransport(server=None, kernel=kernel)

    @staticmethod
    def create_kafka(kernel: RuntimeKernel) -> KafkaTransport:
        from template_app.runtime.transports.kafka.transport import (  # noqa: PLC0415
            KafkaTransport,
        )

        return KafkaTransport(consumer=None, kernel=kernel)
