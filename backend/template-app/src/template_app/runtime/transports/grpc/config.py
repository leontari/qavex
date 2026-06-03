"""gRPC transport configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GRPCTransportConfig:
    """
    gRPC transport configuration.

    Responsibilities:
        - gRPC runtime configuration
        - server binding
        - concurrency tuning
    """

    host: str = "127.0.0.1"

    port: int = 50051

    max_workers: int = 10
