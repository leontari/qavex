"""Runtime graph freeze."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeGraphFreeze:
    """
    Runtime graph freeze state.

    Responsibilities:
        - graph immutability state
        - mutation protection
    """

    frozen: bool = False

    def freeze(self) -> None:
        """Freeze runtime graph."""
        self.frozen = True

    def ensure_mutable(self) -> None:
        """
        Ensure runtime graph is mutable.

        Raises:
            RuntimeError:
                If graph already frozen.

        """
        if self.frozen:
            msg = "Runtime graph has already been frozen."
            raise RuntimeError(msg)
