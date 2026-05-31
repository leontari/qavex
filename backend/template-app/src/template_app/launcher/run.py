"""Application launcher."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.launcher.exceptions import UnsupportedLaunchModeError
from template_app.launcher.modes import LaunchMode
from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.transports.http.entrypoint import run_http_runtime

if TYPE_CHECKING:
    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


@dataclass(slots=True)
class KernelLauncher:
    """
    Runtime kernel launcher.

    ONLY orchestration layer.

    Responsibilities:
        - runtime mode dispatch
        - runtime entrypoint execution

    """

    # _kernel: RuntimeKernel

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
        builder = ApplicationBuilder()

        composition = builder.create()

        # transport creation is externalized
        self._compose(builder, composition)

        builder.freeze(composition)

        # match self._config.mode:
        #     case LaunchMode.HTTP:
        #         self._run_http()
        #     case LaunchMode.KAFKA:
        #         self._run_kafka()
        #     case LaunchMode.GRPC:
        #         self._run_grpc()
        #     case LaunchMode.CLI:
        #         self._run_cli()
        #     case _:
        #         msg = f"Unsupported launch mode: {self._config.mode}"
        #         raise UnsupportedLaunchModeError(msg)

        match self._config.mode:
            case LaunchMode.HTTP:
                run_http_runtime(kernel, self._config)

            case LaunchMode.KAFKA:
                run_kafka_runtime(kernel)

            case LaunchMode.GRPC:
                run_grpc_runtime(kernel)

            case LaunchMode.CLI:
                run_cli_runtime(kernel)

            case _:
                raise UnsupportedLaunchModeError(self._config.mode)

    def _compose(
        self,
        builder,
        composition,
    ) -> None:
        """Compose Hook for DI / plugins later."""
        # intentionally empty
        return

    ################
    # runtime modes
    ################

    def _run_http(self) -> None:
        """Run HTTP runtime."""
        from template_app.runtime.transports.http.entrypoint import (  # noqa: PLC0415
            run_http_runtime,
        )

        run_http_runtime(
            kernel=self._kernel,
            config=self._config,
        )

    def _run_kafka(self) -> None:
        """Run Kafka runtime."""
        from template_app.runtime.transports.kafka.entrypoint import (  # noqa: PLC0415
            run_kafka_runtime,
        )

        run_kafka_runtime(
            kernel=self._kernel,
        )

    def _run_grpc(self) -> None:
        """Run gRPC runtime."""
        from template_app.runtime.transports.grpc.entrypoint import (  # noqa: PLC0415
            run_grpc_runtime,
        )

        run_grpc_runtime(
            kernel=self._kernel,
        )

    def _run_cli(self) -> None:
        """Run CLI runtime."""
        from template_app.runtime.transports.cli.entrypoint import (  # noqa: PLC0415
            run_cli_runtime,
        )

        run_cli_runtime(
            kernel=self._kernel,
        )
