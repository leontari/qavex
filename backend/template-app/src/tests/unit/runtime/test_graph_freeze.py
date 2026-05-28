import pytest

from template_app.runtime.kernel.runtime.graph.freeze import (
    RuntimeGraphFreeze,
)


def test_graph_freeze_blocks_mutation() -> None:
    freeze = RuntimeGraphFreeze()

    freeze.freeze()

    with pytest.raises(RuntimeError):
        freeze.ensure_mutable()
