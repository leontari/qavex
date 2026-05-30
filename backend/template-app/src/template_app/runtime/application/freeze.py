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
        - runtime locking
    """

    @staticmethod
    def freeze(
        composition: ApplicationComposition,
    ) -> None:
        """
        Finalize composition.

        Args:
            composition:
                Mutable application composition.

        """
        kernel = composition.kernel

        for transport in composition.transports:
            kernel.transport_manager.install(
                transport,
            )

        kernel.freeze()
