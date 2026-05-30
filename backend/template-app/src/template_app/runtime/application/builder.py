"""Application builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.runtime.application.composition import (
    ApplicationComposition,
)
from template_app.runtime.application.freeze import (
    ApplicationFreeze,
)
from template_app.runtime.application.installer import (
    TransportInstaller,
)
from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)

if TYPE_CHECKING:
    from template_app.runtime.transports.contracts import (
        Transport,
    )


class ApplicationBuilder:
    """
    Application builder.

    Responsibilities:
        - kernel creation
        - transport composition
        - runtime freeze
    """

    def create(self) -> ApplicationComposition:
        """
        Create composition.

        Returns:
            Mutable application composition.

        """
        return ApplicationComposition(
            kernel=bootstrap_kernel(),
        )

    def install_transport(
        self,
        composition: ApplicationComposition,
        transport: Transport,
    ) -> None:
        """
        Install transport.

        Args:
            composition:
                Mutable composition.

            transport:
                Runtime transport.

        """
        TransportInstaller.install(
            composition,
            transport,
        )

    def freeze(
        self,
        composition: ApplicationComposition,
    ) -> None:
        """
        Freeze application.

        Args:
            composition:
                Mutable composition.

        """
        ApplicationFreeze.freeze(composition)
