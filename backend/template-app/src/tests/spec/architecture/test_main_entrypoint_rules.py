from __future__ import annotations

from pathlib import Path


MAIN_FILE = Path(
    "template_app/main.py",
)


def test_main_does_not_use_builder() -> None:
    source = MAIN_FILE.read_text()

    assert "ApplicationBuilder" not in source


def test_main_does_not_use_bootstrap_kernel() -> None:
    source = MAIN_FILE.read_text()

    assert "bootstrap_kernel" not in source
