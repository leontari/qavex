"""Runtime graph validator."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.runtime.state import RuntimeState


class RuntimeGraphValidator:
    """
    Runtime graph validator.

    Responsibilities:
        - runtime graph validation
        - runtime ownership validation
        - runtime consistency validation
    """

    @staticmethod
    def validate(runtime: RuntimeState) -> None:
        """
        Validate runtime graph.

        Args:
            runtime:
                Runtime graph.

        Raises:
            RuntimeError:
                If runtime graph invalid.

        """
        required = (
            runtime.container,
            runtime.lifecycle,
            runtime.infrastructure,
            runtime.messaging,
            runtime.transports,
            runtime.modules,
        )

        if any(component is None for component in required):
            msg = "Runtime graph contains uninitialized domains."
            raise RuntimeError(msg)
