from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FakeLifecycleHook:
    """
    Runtime-safe lifecycle hook fake.
    """

    executed: bool = field(default=False, init=False)

    calls: int = field(default=0, init=False)

    async def __call__(self) -> None:
        self.executed = True
        self.calls += 1
