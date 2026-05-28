"""Runtime descriptor models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeDescriptor:
    """
    Runtime descriptor.

    Responsibilities:
        - runtime metadata exposure
        - runtime graph introspection
        - runtime diagnostics
    """

    modules: int

    transports: int

    startup_hooks: int

    shutdown_hooks: int

    readiness_probes: int
