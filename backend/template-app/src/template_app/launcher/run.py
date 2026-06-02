"""Application launcher."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.launcher.exceptions import UnsupportedLaunchModeError
from template_app.launcher.modes import LaunchMode
from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.application.composition import (
        ApplicationComposition,
    )


@dataclass(slots=True)
class KernelLauncher:
    """
    Single application composition root.

    FLOW:
    -----
        Launcher
            ↓
        Builder
            ↓
        TransportFactory
            ↓
        Freeze
            ↓
        Runtime

    """

    _config: LauncherConfig

    _composition: ApplicationComposition | None = field(
        default=None,
        init=False,
    )

    def build(self) -> ApplicationComposition:
        """
        Build application once.

        Returns:
            ApplicationComposition

        """
        if self._composition is not None:
            return self._composition

        builder = ApplicationBuilder()

        composition = builder.create()

        self._compose(builder, composition)

        builder.freeze(composition)

        self._composition = composition

        return composition

    def build_http_app(self) -> FastAPI:
        """
        Build FastAPI application.

        Used only by ASGI adapter.

        Returns:
            FastAPI app from composed runtime.

        """
        composition = self.build()

        kernel = composition.kernel

        if not kernel.is_frozen:
            msg = "Kernel must be frozen before transport access"
            raise RuntimeError(msg)

        transport = kernel.transport_manager.get(FastAPITransport)

        if transport is None:
            msg = "HTTP transport is not installed."
            raise RuntimeError(msg)

        return transport.app

    def run(self) -> None:
        """
        Run configured application runtime mode.

        Raises:
            UnsupportedLaunchModeError:
            If runtime mode is unsupported.

        """
        composition = self.build()

        kernel = composition.kernel

        match self._config.mode:
            case LaunchMode.HTTP:
                from template_app.runtime.transports.http.entrypoint import (  # noqa: PLC0415
                    run_http_runtime,
                )

                run_http_runtime(kernel, self._config)

            case LaunchMode.GRPC:
                from template_app.runtime.transports.grpc.entrypoint import (  # noqa: PLC0415
                    run_grpc_runtime,
                )

                run_grpc_runtime(kernel, self._config)

            case LaunchMode.KAFKA:
                from template_app.runtime.transports.kafka.entrypoint import (  # noqa: PLC0415
                    run_kafka_runtime,
                )

                run_kafka_runtime(kernel, self._config)

            case LaunchMode.CLI:
                from template_app.runtime.transports.cli.entrypoint import (  # noqa: PLC0415
                    run_cli_runtime,
                )

                run_cli_runtime(kernel, self._config)

            case _:
                msg = f"Unsupported launch mode: {self._config.mode}"
                raise UnsupportedLaunchModeError(msg)

    def _compose(
        self,
        builder: ApplicationBuilder,
        composition: ApplicationComposition,
    ) -> None:
        """
        Compose runtime transports.

        Future extension point for:
            - plugin discovery
            - module loading
            - DI registration
            - capability registration
        """
        kernel = composition.kernel

        match self._config.mode:
            case LaunchMode.HTTP:
                transport = TransportFactory.create_http(kernel)
                builder.install_transport(composition, transport)

            case LaunchMode.CLI:
                transport = TransportFactory.create_cli(kernel)
                builder.install_transport(composition, transport)

            case LaunchMode.GRPC:
                transport = TransportFactory.create_grpc(kernel)
                builder.install_transport(composition, transport)

            case LaunchMode.KAFKA:
                transport = TransportFactory.create_kafka(kernel)
                builder.install_transport(composition, transport)

            case _:
                return
