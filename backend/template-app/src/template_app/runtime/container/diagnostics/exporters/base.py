from abc import ABC, abstractmethod

from ..snapshot import ContainerSnapshot


class DiagnosticsExporter(ABC):
    """Diagnostics export contract."""

    @abstractmethod
    def export(self, snapshot: ContainerSnapshot) -> str:
        """
        Export diagnostics snapshot.

        Returns:
            Exported representation.

        """
