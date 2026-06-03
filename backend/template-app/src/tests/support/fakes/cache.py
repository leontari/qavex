from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FakeCacheProvider:
    """
    Fake cache infrastructure provider.
    """

    storage: dict[str, object] = field(
        default_factory=dict,
    )

    started: bool = False

    @property
    def name(self) -> str:
        return "cache"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False

    def set(
        self,
        key: str,
        value: object,
    ) -> None:

        self.storage[key] = value

    def get(
        self,
        key: str,
    ) -> object | None:

        return self.storage.get(key)
