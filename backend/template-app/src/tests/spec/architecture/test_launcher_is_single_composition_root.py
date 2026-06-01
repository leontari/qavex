from __future__ import annotations

from pathlib import Path


def test_only_launcher_uses_transport_factory() -> None:

    root = Path("template_app")

    offenders: list[str] = []

    for file in root.rglob("*.py"):

        source = file.read_text()

        if "TransportFactory" not in source:
            continue

        path = str(file)

        if "launcher" not in path:
            offenders.append(path)

    assert offenders == []
