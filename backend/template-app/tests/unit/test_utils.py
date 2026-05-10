from __future__ import annotations

from app.core.utils import normalize_name


def test_normalize_name() -> None:
    assert normalize_name(" Alice ") == "alice"
