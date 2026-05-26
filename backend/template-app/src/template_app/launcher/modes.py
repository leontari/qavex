"""Application launch modes."""

from __future__ import annotations

from enum import StrEnum


class LaunchMode(StrEnum):
    """
    Supported runtime launch modes.

    Launch modes define:
        - runtime topology
        - transport orchestration
        - deployment semantics
        - lifecycle behavior
        - Kubernetes runtime role
    """

    HTTP = "http"

    KAFKA = "kafka"

    GRPC = "grpc"

    CLI = "cli"

    ########################
    # runtime classification
    ########################

    @property
    def is_network_service(self) -> bool:
        """
        Whether runtime exposes external network API.

        Returns:
            True for externally accessible runtimes.

        """
        return self in {
            LaunchMode.HTTP,
            LaunchMode.GRPC,
        }

    @property
    def is_background_worker(self) -> bool:
        """
        Whether runtime acts as background worker.

        Returns:
            True for asynchronous worker runtimes.

        """
        return self is LaunchMode.KAFKA

    @property
    def is_interactive(self) -> bool:
        """
        Whether runtime supports interactive execution.

        Returns:
            True for CLI runtime.

        """
        return self is LaunchMode.CLI

    #########################
    # orchestration semantics
    #########################

    @property
    def requires_readiness(self) -> bool:
        """
        Whether runtime requires readiness probes.

        Returns:
            True for long-running runtimes.

        """
        return self is not LaunchMode.CLI

    @property
    def supports_graceful_shutdown(self) -> bool:
        """
        Whether runtime supports graceful shutdown.

        Returns:
            True for long-running runtimes.

        """
        return self is not LaunchMode.CLI

    @property
    def requires_transport_runtime(self) -> bool:
        """
        Whether runtime requires transport manager.

        Returns:
            True for transport-driven runtimes.

        """
        return self in {
            LaunchMode.HTTP,
            LaunchMode.KAFKA,
            LaunchMode.GRPC,
        }

    #########################
    # kubernetes integration
    #########################

    @property
    def supports_horizontal_scaling(self) -> bool:
        """
        Whether runtime supports Kubernetes scaling.

        Returns:
            True for scalable runtimes.

        """
        return self is not LaunchMode.CLI

    @property
    def supports_probes(self) -> bool:
        """
        Whether runtime exposes health probes.

        Returns:
            True for orchestrated runtimes.

        """
        return self is not LaunchMode.CLI

    ###################
    # parsing utilities
    ###################

    @classmethod
    def from_string(cls, value: str) -> LaunchMode:
        """
        Parse runtime launch mode.

        Args:
            value:
                Raw runtime mode string.

        Returns:
            Parsed launch mode.

        Raises:
            ValueError:
                If launch mode is unsupported.

        """
        normalized = value.strip().lower()

        try:
            return cls(normalized)

        except ValueError as error:
            supported = ", ".join(str(mode) for mode in cls)

            msg = (
                f"Unsupported launch mode '{value}'. "
                f"Supported modes: {supported}"
            )

            raise ValueError(msg) from error

    @classmethod
    def values(cls) -> tuple[str, ...]:
        """
        Return supported launch mode values.

        Returns:
            Tuple containing supported mode names.

        """
        return tuple(str(mode) for mode in cls)

    @property
    def shutdown_timeout_seconds(self) -> int:  # noqa: D102
        raise NotImplementedError

    @property
    def startup_timeout_seconds(self) -> int:  # noqa: D102
        raise NotImplementedError

    @property
    def requires_distributed_lock(self) -> bool:  # noqa: D102
        raise NotImplementedError

    @property
    def supports_leader_election(self) -> bool:  # noqa: D102
        raise NotImplementedError
