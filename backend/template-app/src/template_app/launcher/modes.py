"""
Application launch modes.

LaunchMode defines all supported runtime entrypoints
for the unified multi-transport kernel system.
"""

from __future__ import annotations

from enum import StrEnum


class LaunchMode(StrEnum):
    """
    Supported runtime launch modes.

    Modes:
        HTTP:
            ASGI/REST transport via FastAPI + uvicorn.

        KAFKA:
            Background worker mode consuming Kafka events/messages.

        GRPC:
            gRPC gateway/server transport.

        CLI:
            Interactive/scheduled command execution runtime.
    """

    HTTP = "http"
    KAFKA = "kafka"
    GRPC = "grpc"
    CLI = "cli"

    ########################
    # transport capabilities
    ########################

    @property
    def is_network_transport(self) -> bool:
        """
        Whether mode exposes network transport.

        Returns:
             True for externally exposed network transports.

        """
        return self in {
            LaunchMode.HTTP,
            LaunchMode.GRPC,
        }

    @property
    def is_http(self) -> bool:
        """
        Whether mode exposes HTTP transport.

        Returns:
            True when HTTP transport mode is enabled.

        """
        return self is LaunchMode.HTTP

    @property
    def is_worker(self) -> bool:
        """
        Whether mode acts as background worker.

        Returns:
            True for worker/background modes.

        """
        return self in {
            LaunchMode.KAFKA,
            LaunchMode.CLI,
        }

    @property
    def is_interactive(self) -> bool:
        """
        Whether mode supports interactive execution.

        Returns:
            True for CLI transport mode is enabled.

        """
        return self is LaunchMode.CLI

    #################
    # launch features
    #################

    @property
    def requires_event_loop(self) -> bool:
        """Whether runtime requires asyncio loop."""
        return True

    @property
    def supports_http(self) -> bool:
        """Whether HTTP transport is enabled."""
        return self is LaunchMode.HTTP

    @property
    def supports_grpc(self) -> bool:
        """Whether gRPC transport is enabled."""
        return self is LaunchMode.GRPC

    @property
    def supports_kafka(self) -> bool:
        """Whether Kafka transport is enabled."""
        return self is LaunchMode.KAFKA

    @property
    def supports_cli(self) -> bool:
        """Whether CLI transport is enabled."""
        return self is LaunchMode.CLI

    ###################
    # parsing utilities
    ###################

    @classmethod
    def from_string(cls, value: str) -> "LaunchMode":
        """
        Parse launch mode from string.

        Raises:
            ValueError:
                If mode is unsupported.

        """
        normalized = value.strip().lower()

        try:
            return cls(normalized)

        except ValueError as error:
            supported = ", ".join(mode.value for mode in cls)

            msg = (
                f"Unsupported launch mode '{value}'. "
                f"Supported modes: {supported}"
            )

            raise ValueError(msg) from error

    @classmethod
    def values(cls) -> tuple[str, ...]:
        """Return all available mode values."""
        return tuple(mode.value for mode in cls)
