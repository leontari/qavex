"""
Application installers.

Responsibilities:
    - transport installation
    - module installation
    - plugin installation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.launcher.exceptions import FrozenCompositionError

if TYPE_CHECKING:
    from template_app.runtime.application.composition import (
        ApplicationComposition,
    )
    from template_app.runtime.transports.contracts import Transport


class TransportInstaller:
    """
    Mutable composition installer.

    Allowed only before freeze.

    """

    @staticmethod
    def install(
        composition: ApplicationComposition,
        transport: Transport,
    ) -> None:
        """
        Register transport.

        Args:
            composition:
                Mutable composition.

            transport:
                Runtime transport.

        """
        if composition.kernel.is_frozen:
            msg = "Cannot mutate frozen application composition."
            raise FrozenCompositionError(msg)

        composition.transports.append(transport)
