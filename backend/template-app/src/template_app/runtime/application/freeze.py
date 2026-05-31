"""Application freeze orchestration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.application.composition import (
        ApplicationComposition,
    )


class ApplicationFreeze:
    """
    Freeze application composition.

    Responsibilities:
        - transport materialization
        - runtime locking (freezes kernel)
    """

    @staticmethod
    def freeze(composition: ApplicationComposition) -> None:
        """
        Finalize composition.

        Args:
            composition:
                Mutable application composition.

        """
        kernel = composition.kernel

        # 1. install all transports
        for transport in composition.transports:
            kernel.transport_manager.install(
                transport,
            )

        # 2. freeze kernel AFTER composition
        kernel.freeze()
