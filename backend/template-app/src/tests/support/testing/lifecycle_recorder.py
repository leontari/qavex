from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LifecycleRecorder:
    """
    Runtime lifecycle recorder.

    Responsibilities:
        - execution ordering
        - startup tracking
        - shutdown tracking
        - orchestration assertions
    """

    startup_order: list[str] = field(default_factory=list)

    shutdown_order: list[str] = field(default_factory=list)

    def record_startup(self, name: str) -> None:
        self.startup_order.append(name)

    def record_shutdown(self, name: str) -> None:
        self.shutdown_order.append(name)
