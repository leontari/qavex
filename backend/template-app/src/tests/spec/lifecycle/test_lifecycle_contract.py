from __future__ import annotations


def test_lifecycle_has_registry(lifecycle) -> None:
    """
    Lifecycle runtime must expose registry.
    """
    assert lifecycle.registry is not None
