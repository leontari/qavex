"""Runtime capability models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeCapabilities:
    """
    Runtime capability descriptor.

    Responsibilities:
        - runtime feature declaration
        - runtime capability exposure
        - transport/runtime introspection
    """

    http: bool

    kafka: bool

    grpc: bool

    cli: bool

    lifecycle: bool

    messaging: bool

    infrastructure: bool

    modules: bool
