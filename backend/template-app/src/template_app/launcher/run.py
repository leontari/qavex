"""Application launcher."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.launcher.exceptions import UnsupportedLaunchModeError
from template_app.launcher.modes import LaunchMode

# from template_app.runtime.transports.cli.transport import CLITransport
# from template_app.runtime.transports.grpc.transport import GRPCTransport
# from template_app.runtime.transports.http.factory import create_http_app
# from template_app.runtime.transports.http.transport import FastAPITransport
# from template_app.runtime.transports.kafka.transport import KafkaTransport

if TYPE_CHECKING:
    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


@dataclass(slots=True)
class KernelLauncher:
    """
    Runtime kernel launcher.

    Responsibilities:
        - runtime mode dispatch
        - runtime entrypoint execution

    """

    _kernel: RuntimeKernel

    _config: LauncherConfig

    #################
    # public Launcher
    #################

    def run(self) -> None:
        """
        Run configured runtime mode.

        Raises:
            UnsupportedLaunchModeError:
            If runtime mode is unsupported.

        """
        match self._config.mode:
            case LaunchMode.HTTP:
                self._run_http()
            case LaunchMode.KAFKA:
                self._run_kafka()
            case LaunchMode.GRPC:
                self._run_grpc()
            case LaunchMode.CLI:
                self._run_cli()
            case _:
                msg = f"Unsupported launch mode: {self._config.mode}"
                raise UnsupportedLaunchModeError(msg)

    ################
    # runtime modes
    ################

    def _run_http(self) -> None:
        """Run HTTP runtime."""
        from template_app.runtime.transports.http.entrypoint import (
            run_http_runtime,
        )

        run_http_runtime(
            kernel=self._kernel,
            config=self._config,
        )
        # app = create_http_app(self._kernel)
        #
        # transport = FastAPITransport(app)
        # # transport = FastAPITransport(app, self.kernel)
        # self._kernel.install_transport(transport)
        #
        # import uvicorn  # noqa: PLC0415
        #
        # uvicorn.run(
        #     app,
        #     host=self._config.host,
        #     port=self._config.port,
        #     reload=self._config.reload,
        #     workers=self._config.workers,
        # )

    def _run_kafka(self) -> None:
        """Run Kafka runtime."""
        from template_app.runtime.transports.kafka.entrypoint import (
            run_kafka_runtime,
        )

        run_kafka_runtime(
            kernel=self._kernel,
        )

    def _run_grpc(self) -> None:
        """Run gRPC runtime."""
        from template_app.runtime.transports.grpc.entrypoint import (
            run_grpc_runtime,
        )

        run_grpc_runtime(kernel=self._kernel)

    def _run_cli(self) -> None:
        """Run CLI runtime."""
        from template_app.runtime.transports.cli.entrypoint import (
            run_cli_runtime,
        )
