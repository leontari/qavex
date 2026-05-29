from __future__ import annotations

import importlib


def test_package_import_is_side_effect_safe() -> None:
    """
    Importing package must not crash runtime.
    """

    module = importlib.import_module(
        "template_app",
    )

    assert module is not None
