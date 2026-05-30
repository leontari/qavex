"""
Application installers.

Responsibilities:
    - transport installation
    - module installation
    - plugin installation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.application.composition import (
        ApplicationComposition,
    )
    from template_app.runtime.transports.contracts import Transport


class TransportInstaller:
    """
    Transport installer.

    Responsibilities:
        - transport registration
        - composition ownership
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
        composition.transports.append(transport)
