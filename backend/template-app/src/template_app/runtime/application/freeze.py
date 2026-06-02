"""Application freeze orchestration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.application.composition import (
        ApplicationComposition,
    )


class ApplicationFreeze:
    """
    Final application freeze phase.

    Responsibilities:
        - transport materialization (install transports)
        - runtime locking (freezes runtime kernel graph)
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

        if kernel.is_frozen:
            return

        # 1. install all transports
        for transport in composition.transports:
            kernel.install_transport(transport)

        # 2. freeze kernel AFTER composition
        kernel.freeze()
